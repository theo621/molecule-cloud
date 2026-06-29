"""Excel input handling for molecule cloud."""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple


class ExcelReader:
    """Read and parse Excel files with scaffold data."""

    def __init__(self, excel_file: str):
        """Initialize Excel reader.

        Args:
            excel_file: Path to Excel file
        """
        self.excel_file = Path(excel_file)
        if not self.excel_file.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_file}")

    def read(self) -> pd.DataFrame:
        """Read Excel file.

        Expected columns:
        - SMILES: SMILES string of the molecule
        - Activity: Positive (1) or Negative (0) or boolean
        - [Optional] Frequency: Pre-computed frequency

        Returns:
            DataFrame with parsed data
        """
        df = pd.read_excel(self.excel_file)

        # Validate required columns
        if "SMILES" not in df.columns:
            raise ValueError("Excel file must contain 'SMILES' column")

        if "Activity" not in df.columns:
            raise ValueError("Excel file must contain 'Activity' column")

        # Normalize Activity column
        df["Activity"] = df["Activity"].astype(int)

        return df
