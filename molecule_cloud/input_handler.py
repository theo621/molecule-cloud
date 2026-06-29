"""Input handling for scaffold data (Excel and CSV)."""

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
        - Toxicity or Activity: Positive (1) or Negative (0) or boolean
        - [Optional] Scaffold: Pre-computed scaffold

        Returns:
            DataFrame with parsed data
        """
        df = pd.read_excel(self.excel_file)

        # Validate required columns
        if "SMILES" not in df.columns:
            raise ValueError("Excel file must contain 'SMILES' column")

        # Check for Activity or Toxicity column
        if "Toxicity" in df.columns:
            # Rename Toxicity to Activity for consistency
            df["Activity"] = df["Toxicity"]
        elif "Activity" in df.columns:
            pass  # Already has Activity column
        else:
            raise ValueError("Excel file must contain 'Toxicity' or 'Activity' column")

        # If Scaffold column exists, use it instead of SMILES
        if "Scaffold" in df.columns:
            df_clean = pd.DataFrame({
                'SMILES': df['Scaffold'],
                'Activity': df['Activity']
            })
        else:
            df_clean = pd.DataFrame({
                'SMILES': df['SMILES'],
                'Activity': df['Activity']
            })

        # Remove empty rows
        df_clean = df_clean.dropna(subset=['SMILES'])
        df_clean = df_clean[df_clean['SMILES'].astype(str).str.strip() != '']

        # Normalize Activity column
        df_clean["Activity"] = df_clean["Activity"].astype(int)

        return df_clean


class CSVReader:
    """Read and parse CSV files with scaffold data."""

    def __init__(self, csv_file: str):
        """Initialize CSV reader.

        Args:
            csv_file: Path to CSV file
        """
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

    def read(self) -> pd.DataFrame:
        """Read CSV file.

        Expected columns:
        - SMILES: SMILES string of the molecule
        - Activity or Toxicity: Positive (1) or Negative (0) or boolean
        - [Optional] Additional columns ignored

        Returns:
            DataFrame with parsed data
        """
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(self.csv_file, encoding=encoding)
                break
            except (UnicodeDecodeError, Exception):
                continue
        
        if df is None:
            raise ValueError(f"Could not read CSV file with any encoding: {encodings}")

        # Validate required columns
        col_names = list(df.columns)
        
        if len(col_names) < 2:
            raise ValueError(f"CSV file must have at least 2 columns. Found: {col_names}")

        # Auto-map columns: assume first 3 columns are SMILES, Activity, Scaffold
        # Rename to standard format
        col_smiles = col_names[0]
        col_activity = col_names[1]
        col_scaffold = col_names[2] if len(col_names) > 2 else None

        # Use Scaffold column if available, otherwise use SMILES
        if col_scaffold is not None:
            df_clean = pd.DataFrame({
                'SMILES': df[col_scaffold],
                'Activity': df[col_activity]
            })
        else:
            df_clean = pd.DataFrame({
                'SMILES': df[col_smiles],
                'Activity': df[col_activity]
            })

        # Remove empty rows
        df_clean = df_clean.dropna(subset=['SMILES'])
        df_clean = df_clean[df_clean['SMILES'].astype(str).str.strip() != '']

        # Normalize Activity column
        df_clean["Activity"] = df_clean["Activity"].astype(int)

        return df_clean


class DataReader:
    """Universal reader for Excel and CSV files."""

    @staticmethod
    def read(file_path: str) -> pd.DataFrame:
        """Read Excel or CSV file automatically.

        Args:
            file_path: Path to file (.xlsx, .xls, or .csv)

        Returns:
            DataFrame with parsed data
        """
        file_path_str = str(file_path).lower()

        if file_path_str.endswith('.csv'):
            reader = CSVReader(file_path)
            return reader.read()
        elif file_path_str.endswith(('.xlsx', '.xls')):
            reader = ExcelReader(file_path)
            return reader.read()
        else:
            raise ValueError(f"Unsupported file format: {file_path}. Use .csv or .xlsx")
