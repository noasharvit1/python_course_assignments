# QM9 HOMO-LUMO Gap Prediction

---

## Overview

This project analyses a **5 000-molecule subset of the QM9 dataset** and trains machine-learning
models to predict the **HOMO-LUMO gap** (an important electronic property) from simple
hand-crafted molecular features (atom counts, bond statistics, elemental fractions).

| Property predicted | HOMO-LUMO gap |
|--------------------|---------------|
| Unit               | eV            |
| QM9 column index   | 4             |
| ML models          | Random Forest, Gradient Boosting |

---

## Project Structure

```
day09/
├── qm9_analysis.py   # Main script: data loading, feature engineering, ML, plots
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── outputs/          # Created automatically when the script runs
    ├── eda_plots.png
    └── model_results.png
```

---

## Prerequisites

- Python 3.10 or 3.11 (recommended)
- pip ≥ 23

---

## Installation

### 1 · Clone / download this project

```bash
# If using git
git clone <your-repo-url>
cd qm9_project

# Or just place the files in a folder and cd into it
```

### 2 · Create a virtual environment (recommended)

```bash
python -m venv .venv

# Activate – Linux / macOS
source .venv/bin/activate

# Activate – Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3 · Install dependencies

PyTorch must be installed **before** the rest of the packages, because
`torch-geometric` depends on it at build time. Run these two commands in order:

```bash
# Step 1 – install PyTorch first (CPU-only wheel)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Step 2 – install everything else (including torch-geometric)
pip install -r requirements.txt
```

---

## Downloading the Dataset

The QM9 dataset is downloaded **automatically** the first time the script runs via
`torch_geometric.datasets.QM9`.  It will be saved to `./data/` (~200 MB).

If you prefer a manual download:

1. Visit https://figshare.com/collections/Quantum_chemistry_structures_and_properties_of_134_kilo_molecules/978904
2. Download `dsgdb9nsd.xyz.tar.bz2`
3. Pass the extraction folder as `root` in `load_qm9_subset(root="<path>")`.

---

## Running the Script

```bash
python qm9_analysis.py
```

Expected runtime: **~2–5 minutes** on a modern laptop (CPU-only).

The script will print a progress log and a final summary table, e.g.:

```
============================================================
  QM9 HOMO-LUMO Gap Prediction
============================================================
[1] Loading QM9 subset (5000 molecules)...
[2] Extracting features...
[3] Generating EDA plots...
[4] Training models...

  Training Random Forest...
    MAE  = 0.4821 eV
    RMSE = 0.6104 eV
    R²   = 0.7312
  Training Gradient Boosting...
    ...
[5] Generating result plots...
[6] Summary
----------------------------------------------------
Model                    MAE    RMSE      R²    CV R²
----------------------------------------------------
Random Forest          0.4821  0.6104  0.7312  0.721±0.014
Gradient Boosting      0.4503  0.5847  0.7541  0.748±0.012
----------------------------------------------------
```

Output images are saved to `./outputs/`.

---

## Prompts Used (Assignment Requirement)

I used Claude (claude.ai) to generate this project.
https://claude.ai/new

---


"I am an MSc student in chemistry, and I am taking a course in Python. I received the following assignment:

1. Pick a dataset that you would like to analyze. You can use one from your lab, ask you to recommend one, or download one from Kaggle or any other source that you find appealing.
2. Create a prediction based on the data.
3. Add a README file with clear instructions on how to download the dataset and rerun the example. Please include your prompts as well. 

I need help implementing this assignment using The QM9 Dataset Subset"

---

## Results Interpretation

- **EDA plots** show the distribution of the HOMO-LUMO gap, molecular sizes,
  elemental composition, and feature–target correlations.
- **Parity plots** (predicted vs. true) illustrate model accuracy; points on
  the diagonal indicate perfect prediction.
- **Residual plot** helps diagnose systematic bias (non-random patterns → model misfit).
- **Feature importance** reveals which molecular descriptors drive the prediction.

---

## References

1. Ramakrishnan, R. et al. *Quantum chemistry structures and properties of 134 kilo molecules.*
   Scientific Data **1**, 140022 (2014). https://doi.org/10.1038/sdata.2014.22
2. Ruddigkeit, L. et al. *Enumeration of 166 billion organic small molecules in the chemical
   universe database GDB-17.* J. Chem. Inf. Model. **52**, 2864–2875 (2012).
3. Fey, M. & Lenssen, J. E. *Fast graph representation learning with PyTorch Geometric.*
   ICLR Workshop on Representation Learning on Graphs and Manifolds (2019).
