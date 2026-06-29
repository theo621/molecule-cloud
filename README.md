# Molecule Cloud

A Python implementation of Molecule Cloud visualization inspired by Peter Ertl's work on scaffold analysis. This tool generates cloud-like visualizations of molecular scaffolds with sizes proportional to their frequency in the dataset.

## Features

- **Scaffold Input**: Read molecular scaffolds from Excel files
- **Classification**: Automatic split of positive and negative samples
- **Aggregation**: Duplicate scaffold detection and merging
- **Scaling**: Visual size proportional to sqrt(frequency)
- **Visualization**:
  - RDKit-based chemical structure rendering
  - Whitespace cropping for compact images
  - Spiral placement algorithm for initial positioning
  - Collision avoidance with force-directed relaxation
  - Compaction optimization
  - Pastel-colored rectangles as backgrounds
- **Export Formats**: PNG and SVG output
- **Reproducibility**: Deterministic random seed control

## Installation

```bash
pip install molecule-cloud
```

## Usage

```python
from molecule_cloud import MoleculeCloud

# Create cloud from Excel file
cloud = MoleculeCloud(excel_file='scaffolds.xlsx')

# Generate visualization
cloud.generate()

# Export
cloud.export_png('output.png')
cloud.export_svg('output.svg')
```

## Requirements

- Python 3.8+
- RDKit
- Pandas
- NumPy
- Pillow
- openpyxl

## References

Ertl, P. (2009). Scaffold Hunter: A tool for mining bioactive scaffolds and exploring structure–activity relationships. *Journal of Chemical Information and Modeling*, 49(4), 783-790.
