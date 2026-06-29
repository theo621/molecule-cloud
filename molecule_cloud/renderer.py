"""RDKit rendering utilities for molecular structures."""

import numpy as np
from PIL import Image, ImageDraw
from typing import Tuple, Optional

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
except ImportError:
    raise ImportError("RDKit is required. Install with: pip install rdkit")


class MoleculeRenderer:
    """Render molecular structures using RDKit."""

    def __init__(self, size: int = 200, kekulize: bool = True):
        """Initialize renderer.

        Args:
            size: Output image size in pixels
            kekulize: Apply Kekule form
        """
        self.size = size
        self.kekulize = kekulize

    def render_molecule(self, smiles: str) -> Optional[Image.Image]:
        """Render a single molecule from SMILES.

        Args:
            smiles: SMILES string

        Returns:
            PIL Image or None if parsing fails
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return None

            if self.kekulize:
                Chem.Kekulize(mol, clearAromaticFlags=False)

            img = Draw.MolToImage(mol, size=(self.size, self.size))
            return img
        except Exception as e:
            print(f"Error rendering {smiles}: {e}")
            return None

    def crop_whitespace(self, image: Image.Image) -> Image.Image:
        """Crop whitespace from image.

        Args:
            image: PIL Image

        Returns:
            Cropped image
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Find bounding box of non-white pixels
        pixels = image.load()
        white = (255, 255, 255)

        min_x, min_y = image.width, image.height
        max_x, max_y = 0, 0

        for y in range(image.height):
            for x in range(image.width):
                if pixels[x, y][:3] != white:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        if min_x >= max_x or min_y >= max_y:
            return image

        # Crop with small padding
        padding = 5
        bbox = (
            max(0, min_x - padding),
            max(0, min_y - padding),
            min(image.width, max_x + padding),
            min(image.height, max_y + padding),
        )

        return image.crop(bbox)

    def render_with_background(
        self,
        smiles: str,
        color: Tuple[int, int, int] = (200, 200, 200),
        size: int = 150,
    ) -> Optional[Image.Image]:
        """Render molecule with pastel background rectangle.

        Args:
            smiles: SMILES string
            color: RGB color tuple (pastel)
            size: Target size

        Returns:
            PIL Image with background
        """
        mol_img = self.render_molecule(smiles)
        if mol_img is None:
            return None

        # Crop whitespace
        mol_img = self.crop_whitespace(mol_img)

        # Create background
        bg = Image.new('RGB', (size, size), color)

        # Paste molecule centered
        paste_x = (size - mol_img.width) // 2
        paste_y = (size - mol_img.height) // 2
        bg.paste(mol_img, (paste_x, paste_y))

        return bg
