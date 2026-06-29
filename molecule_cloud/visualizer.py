"""Visualization and export functionality."""

import numpy as np
import svgwrite
from PIL import Image, ImageDraw
from typing import Dict, List, Optional

from .renderer import MoleculeRenderer
from .colors import get_pastel_colors


class CloudVisualizer:
    """Compose and export molecule cloud visualizations."""

    def __init__(self, canvas_width: int = 1200, canvas_height: int = 800):
        """Initialize visualizer.

        Args:
            canvas_width: Canvas width in pixels
            canvas_height: Canvas height in pixels
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.renderer = MoleculeRenderer(size=200)
        self.color_palette = get_pastel_colors()

    def render_scaffolds(self, scaffold_collection, positions):
        """Render all scaffolds.

        Args:
            scaffold_collection: ScaffoldCollection object
            positions: Array of (x, y) positions

        Returns:
            Dict mapping scaffold SMILES to rendered Image
        """
        rendered = {}
        scaffolds = scaffold_collection.get_scaffolds_list()

        for i, scaffold in enumerate(scaffolds):
            size = int(scaffold.size * 60)
            color_idx = i % len(self.color_palette)
            color = self.color_palette[color_idx]

            img = self.renderer.render_with_background(
                scaffold.smiles,
                color=color,
                size=size,
            )

            if img is not None:
                rendered[scaffold.smiles] = img

        return rendered

    def compose_image(
        self,
        scaffold_collection,
        positions,
        rendered_scaffolds,
        format: str = "PNG",
    ) -> Image.Image:
        """Compose final image.

        Args:
            scaffold_collection: ScaffoldCollection object
            positions: Array of (x, y) positions
            rendered_scaffolds: Dict of rendered Images
            format: Output format

        Returns:
            PIL Image
        """
        # Create canvas
        canvas = Image.new('RGB', (self.canvas_width, self.canvas_height), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Paste rendered scaffolds
        scaffolds = scaffold_collection.get_scaffolds_list()
        for i, scaffold in enumerate(scaffolds):
            if scaffold.smiles not in rendered_scaffolds:
                continue

            img = rendered_scaffolds[scaffold.smiles]
            x, y = positions[i]

            # Center the image
            paste_x = int(x - img.width / 2)
            paste_y = int(y - img.height / 2)

            canvas.paste(img, (paste_x, paste_y))

        return canvas

    def export_svg(
        self,
        scaffold_collection,
        positions,
        rendered_scaffolds,
        output_path: str,
    ) -> None:
        """Export as SVG.

        Args:
            scaffold_collection: ScaffoldCollection object
            positions: Array of (x, y) positions
            rendered_scaffolds: Dict of rendered Images
            output_path: Output file path
        """
        dwg = svgwrite.Drawing(output_path, size=(self.canvas_width, self.canvas_height))

        # Add white background
        dwg.add(dwg.rect(insert=(0, 0), size=(self.canvas_width, self.canvas_height), fill='white'))

        # Add scaffolds as embedded images
        scaffolds = scaffold_collection.get_scaffolds_list()
        for i, scaffold in enumerate(scaffolds):
            if scaffold.smiles not in rendered_scaffolds:
                continue

            img = rendered_scaffolds[scaffold.smiles]
            x, y = positions[i]

            # Convert image to base64
            import base64
            from io import BytesIO

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()

            # Add image to SVG
            paste_x = x - img.width / 2
            paste_y = y - img.height / 2

            dwg.add(dwg.image(
                href=f'data:image/png;base64,{img_base64}',
                insert=(paste_x, paste_y),
                size=(img.width, img.height),
            ))

        dwg.save()
