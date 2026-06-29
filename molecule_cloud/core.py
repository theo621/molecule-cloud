"""Main MoleculeCloud class for orchestrating the visualization pipeline."""

import random
import numpy as np
from pathlib import Path
from typing import Optional, Tuple

from .input_handler import ExcelReader
from .scaffold import ScaffoldCollection
from .layout import LayoutEngine
from .visualizer import CloudVisualizer


class MoleculeCloud:
    """Main class for creating molecule cloud visualizations."""

    def __init__(
        self,
        excel_file: str,
        random_seed: int = 42,
        canvas_width: int = 1200,
        canvas_height: int = 800,
    ):
        """Initialize MoleculeCloud.

        Args:
            excel_file: Path to Excel file with scaffold data
            random_seed: Seed for reproducible randomization
            canvas_width: Width of output canvas in pixels
            canvas_height: Height of output canvas in pixels
        """
        self.random_seed = random_seed
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self._set_seed()

        # Load and process data
        reader = ExcelReader(excel_file)
        self.data = reader.read()

        # Create scaffold collection
        self.scaffolds = ScaffoldCollection(self.data)
        self.scaffolds.aggregate_duplicates()
        self.scaffolds.scale_by_frequency()

        # Initialize layout engine
        self.layout_engine = LayoutEngine(
            canvas_width=canvas_width,
            canvas_height=canvas_height,
            random_seed=random_seed,
        )

        # Initialize visualizer
        self.visualizer = CloudVisualizer(
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )

        self.positions = None
        self.rendered_scaffolds = None

    def _set_seed(self) -> None:
        """Set random seed for reproducibility."""
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

    def generate(
        self,
        use_force_relaxation: bool = True,
        use_compaction: bool = True,
    ) -> None:
        """Generate the molecule cloud layout.

        Args:
            use_force_relaxation: Apply force-directed relaxation
            use_compaction: Apply compaction optimization
        """
        # Initial spiral placement
        self.positions = self.layout_engine.spiral_placement(self.scaffolds.get_sizes())

        # Collision avoidance
        self.positions = self.layout_engine.collision_avoidance(
            self.positions, self.scaffolds.get_sizes()
        )

        # Force-directed relaxation
        if use_force_relaxation:
            self.positions = self.layout_engine.force_directed_relaxation(
                self.positions, self.scaffolds.get_sizes()
            )

        # Compaction
        if use_compaction:
            self.positions = self.layout_engine.compaction(self.positions)

        # Render scaffold images
        self.rendered_scaffolds = self.visualizer.render_scaffolds(
            self.scaffolds, self.positions
        )

    def export_png(self, output_path: str) -> None:
        """Export cloud visualization as PNG.

        Args:
            output_path: Path for output PNG file
        """
        if self.rendered_scaffolds is None:
            raise RuntimeError("Must call generate() before export")

        image = self.visualizer.compose_image(
            self.scaffolds, self.positions, self.rendered_scaffolds, format="PNG"
        )
        image.save(output_path, "PNG")

    def export_svg(self, output_path: str) -> None:
        """Export cloud visualization as SVG.

        Args:
            output_path: Path for output SVG file
        """
        if self.rendered_scaffolds is None:
            raise RuntimeError("Must call generate() before export")

        self.visualizer.export_svg(
            self.scaffolds, self.positions, self.rendered_scaffolds, output_path
        )
