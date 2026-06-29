from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="molecule-cloud",
    version="0.1.0",
    author="Theo",
    description="Molecule Cloud visualization inspired by Peter Ertl's scaffold analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rdkit>=2023.03.1",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "Pillow>=8.0.0",
        "openpyxl>=3.0.0",
        "svgwrite>=1.4.0",
    ],
)
