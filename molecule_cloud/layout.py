"""Layout algorithms for positioning scaffolds."""

import numpy as np
import random
from typing import Tuple
from tqdm import tqdm


class LayoutEngine:
    """Handles layout algorithms for molecule cloud."""

    def __init__(
        self,
        canvas_width: int = 1200,
        canvas_height: int = 800,
        random_seed: int = 42,
    ):
        """Initialize layout engine.

        Args:
            canvas_width: Canvas width in pixels
            canvas_height: Canvas height in pixels
            random_seed: Seed for reproducibility
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)

    def spiral_placement(self, sizes: np.ndarray) -> np.ndarray:
        """Place items in a spiral pattern.

        Args:
            sizes: Array of item sizes

        Returns:
            Array of (x, y) positions
        """
        n = len(sizes)
        positions = np.zeros((n, 2))

        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2

        for i in range(n):
            # Archimedean spiral
            angle = i * 0.5  # Adjust for density
            radius = 10 + i * 2  # Gradually increase radius

            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)

            # Clamp to canvas
            x = np.clip(x, sizes[i] * 25, self.canvas_width - sizes[i] * 25)
            y = np.clip(y, sizes[i] * 25, self.canvas_height - sizes[i] * 25)

            positions[i] = [x, y]

        return positions

    def collision_avoidance(
        self, positions: np.ndarray, sizes: np.ndarray, max_iterations: int = 50
    ) -> np.ndarray:
        """Avoid collisions between items.

        Args:
            positions: Current positions
            sizes: Item sizes
            max_iterations: Maximum iterations

        Returns:
            Adjusted positions
        """
        positions = positions.copy()

        for iteration in tqdm(range(max_iterations), desc="   🔄 Collision avoidance", unit="iter", leave=False):
            moved = False

            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    dx = positions[j, 0] - positions[i, 0]
                    dy = positions[j, 1] - positions[i, 1]
                    dist = np.sqrt(dx**2 + dy**2)

                    # Minimum distance based on sizes
                    min_dist = (sizes[i] + sizes[j]) * 25

                    if dist < min_dist:
                        # Push apart
                        if dist > 0:
                            overlap = min_dist - dist
                            push_x = (dx / dist) * overlap * 0.5
                            push_y = (dy / dist) * overlap * 0.5
                        else:
                            # Random push if exactly overlapping
                            angle = random.random() * 2 * np.pi
                            push_x = np.cos(angle) * 5
                            push_y = np.sin(angle) * 5

                        positions[i, 0] -= push_x
                        positions[i, 1] -= push_y
                        positions[j, 0] += push_x
                        positions[j, 1] += push_y
                        moved = True

            if not moved:
                break

        # Clamp to canvas
        for i in range(len(positions)):
            positions[i, 0] = np.clip(positions[i, 0], sizes[i] * 25, self.canvas_width - sizes[i] * 25)
            positions[i, 1] = np.clip(positions[i, 1], sizes[i] * 25, self.canvas_height - sizes[i] * 25)

        return positions

    def force_directed_relaxation(
        self,
        positions: np.ndarray,
        sizes: np.ndarray,
        k: float = 0.1,
        iterations: int = 100,
    ) -> np.ndarray:
        """Apply force-directed relaxation to layout.

        Args:
            positions: Current positions
            sizes: Item sizes
            k: Force constant
            iterations: Number of iterations

        Returns:
            Relaxed positions
        """
        positions = positions.copy().astype(float)
        velocities = np.zeros_like(positions)
        damping = 0.9

        for iteration in tqdm(range(iterations), desc="   ⚡ Force-directed relaxation", unit="iter"):
            forces = np.zeros_like(positions)

            for i in range(len(positions)):
                for j in range(len(positions)):
                    if i == j:
                        continue

                    dx = positions[j, 0] - positions[i, 0]
                    dy = positions[j, 1] - positions[i, 1]
                    dist = np.sqrt(dx**2 + dy**2 + 1e-6)

                    # Repulsive force
                    min_dist = (sizes[i] + sizes[j]) * 25
                    if dist < min_dist * 2:
                        fx = -(dx / dist) * k * 10
                        fy = -(dy / dist) * k * 10
                        forces[i] += [fx, fy]

            velocities = velocities * damping + forces
            positions += velocities * 0.1

            # Clamp to canvas
            for i in range(len(positions)):
                positions[i, 0] = np.clip(positions[i, 0], sizes[i] * 25, self.canvas_width - sizes[i] * 25)
                positions[i, 1] = np.clip(positions[i, 1], sizes[i] * 25, self.canvas_height - sizes[i] * 25)

        return positions

    def compaction(self, positions: np.ndarray, iterations: int = 10) -> np.ndarray:
        """Compact layout by moving items closer.

        Args:
            positions: Current positions
            iterations: Number of iterations

        Returns:
            Compacted positions
        """
        positions = positions.copy().astype(float)

        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2

        for iteration in tqdm(range(iterations), desc="   📦 Compaction", unit="iter", leave=False):
            for i in range(len(positions)):
                # Move towards center with decay
                dx = center_x - positions[i, 0]
                dy = center_y - positions[i, 1]
                positions[i, 0] += dx * 0.01
                positions[i, 1] += dy * 0.01

        return positions
