"""Scaffold data structures and operations."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import Counter
import numpy as np


@dataclass
class Scaffold:
    """Represents a single molecular scaffold."""

    smiles: str
    frequency: int = 1
    positive_count: int = 0
    negative_count: int = 0
    size: float = 1.0  # Scaled size for visualization
    color: Tuple[int, int, int] = field(default=(200, 200, 200))

    @property
    def activity_ratio(self) -> float:
        """Calculate ratio of positive to total samples."""
        total = self.positive_count + self.negative_count
        return self.positive_count / total if total > 0 else 0.5


class ScaffoldCollection:
    """Collection of molecular scaffolds with aggregation and scaling."""

    def __init__(self, data):
        """Initialize from pandas DataFrame.

        Args:
            data: DataFrame with SMILES, Activity columns
        """
        self.scaffolds: Dict[str, Scaffold] = {}
        self._initialize_from_data(data)

    def _initialize_from_data(self, data) -> None:
        """Initialize scaffolds from data."""
        for _, row in data.iterrows():
            smiles = row["SMILES"]
            activity = int(row["Activity"])

            if smiles not in self.scaffolds:
                self.scaffolds[smiles] = Scaffold(smiles=smiles)

            scaffold = self.scaffolds[smiles]
            scaffold.frequency += 1

            if activity == 1:
                scaffold.positive_count += 1
            else:
                scaffold.negative_count += 1

    def aggregate_duplicates(self) -> None:
        """Aggregate duplicate scaffolds (already done in init)."""
        pass

    def scale_by_frequency(self, min_scale: float = 0.5, max_scale: float = 3.0) -> None:
        """Scale scaffold size by square root of frequency.

        Args:
            min_scale: Minimum scaling factor
            max_scale: Maximum scaling factor
        """
        if not self.scaffolds:
            return

        frequencies = [s.frequency for s in self.scaffolds.values()]
        sqrt_freqs = np.sqrt(frequencies)

        min_freq = sqrt_freqs.min()
        max_freq = sqrt_freqs.max()
        freq_range = max_freq - min_freq if max_freq > min_freq else 1

        for scaffold in self.scaffolds.values():
            normalized = (np.sqrt(scaffold.frequency) - min_freq) / freq_range
            scaffold.size = min_scale + normalized * (max_scale - min_scale)

    def get_sizes(self) -> np.ndarray:
        """Get array of scaffold sizes for layout.

        Returns:
            Array of sizes
        """
        return np.array([s.size for s in self.scaffolds.values()])

    def get_scaffolds_list(self) -> List[Scaffold]:
        """Get list of scaffolds.

        Returns:
            List of Scaffold objects
        """
        return list(self.scaffolds.values())

    def __len__(self) -> int:
        """Return number of unique scaffolds."""
        return len(self.scaffolds)
