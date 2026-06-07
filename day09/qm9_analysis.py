"""
QM9 Dataset Subset Analysis and HOMO-LUMO Gap Prediction
=========================================================
MSc Chemistry - Python Course Assignment

This script:
1. Downloads a QM9 subset (first 5000 molecules) via PyTorch Geometric
2. Extracts molecular features (atom counts, bond statistics)
3. Trains a Random Forest model to predict the HOMO-LUMO gap (property index 4)
4. Evaluates performance with MAE, RMSE, and R² metrics
5. Generates and saves plots for exploratory data analysis and model evaluation
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import Counter

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load QM9 Subset ────────────────────────────────────────────────────────

def load_qm9_subset(root="./data", subset_size=5000):
    """
    Load a subset of QM9 via PyTorch Geometric.
    QM9 contains 130,831 molecules with up to 9 heavy atoms (C, H, O, N, F).
    """
    print(f"Loading QM9 subset ({subset_size} molecules)...")
    try:
        from torch_geometric.datasets import QM9
    except ImportError:
        raise ImportError(
            "PyTorch Geometric is required. Install it with:\n"
            "  pip install torch torch-geometric\n"
            "See README.md for full instructions."
        )

    dataset = QM9(root=root)
    subset = dataset[:subset_size]
    print(f"  Loaded {len(subset)} molecules.")
    return subset


# ── 2. Feature Engineering ────────────────────────────────────────────────────

# Atomic number → element symbol
ATOMIC_NUMBER_TO_SYMBOL = {1: "H", 6: "C", 7: "N", 8: "O", 9: "F"}

def extract_features(dataset):
    """
    Extract hand-crafted molecular features from each Data object.

    Features per molecule
    ---------------------
    - num_atoms          : total atom count
    - num_bonds          : total (directed) edge count / 2
    - count_H/C/N/O/F    : per-element atom counts
    - frac_H/C/N/O/F     : per-element atom fractions
    - avg_degree         : mean bonds per atom
    - max_degree         : maximum bonds per any atom
    - bond_density       : bonds / (atoms*(atoms-1)/2)  – graph density
    """
    rows = []
    targets = []

    for data in dataset:
        z = data.z.numpy()          # atomic numbers, shape (N,)
        edge_index = data.edge_index.numpy()  # shape (2, E)
        n_atoms = len(z)
        n_bonds = edge_index.shape[1] // 2   # undirected

        counts = Counter(z.tolist())
        feats = {
            "num_atoms": n_atoms,
            "num_bonds": n_bonds,
        }
        for an, sym in ATOMIC_NUMBER_TO_SYMBOL.items():
            feats[f"count_{sym}"] = counts.get(an, 0)
            feats[f"frac_{sym}"]  = counts.get(an, 0) / n_atoms

        # Degree statistics
        degrees = np.bincount(edge_index[0], minlength=n_atoms)
        feats["avg_degree"]    = degrees.mean()
        feats["max_degree"]    = degrees.max()
        max_possible_bonds     = n_atoms * (n_atoms - 1) / 2
        feats["bond_density"]  = n_bonds / max_possible_bonds if max_possible_bonds > 0 else 0.0

        rows.append(feats)

        # Target: HOMO-LUMO gap (index 4), convert from Hartree → eV  (1 Ha = 27.2114 eV)
        homo_lumo_gap_ev = float(data.y[0, 4]) * 27.2114
        targets.append(homo_lumo_gap_ev)

    X = pd.DataFrame(rows)
    y = np.array(targets)
    print(f"  Feature matrix: {X.shape}  |  Target vector: {y.shape}")
    return X, y


# ── 3. Exploratory Data Analysis ──────────────────────────────────────────────

def plot_eda(X, y, save_path="eda_plots.png"):
    """Generate a 2×3 grid of exploratory plots."""
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("QM9 Subset – Exploratory Data Analysis", fontsize=16, fontweight="bold", y=1.01)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.35)

    # 1. HOMO-LUMO gap distribution
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(y, bins=60, color="#4C72B0", edgecolor="white", linewidth=0.4)
    ax1.axvline(y.mean(), color="tomato", linestyle="--", label=f"Mean = {y.mean():.2f} eV")
    ax1.set_xlabel("HOMO-LUMO Gap (eV)")
    ax1.set_ylabel("Count")
    ax1.set_title("HOMO-LUMO Gap Distribution")
    ax1.legend(fontsize=9)

    # 2. Atom count distribution
    ax2 = fig.add_subplot(gs[0, 1])
    atom_counts = X["num_atoms"].value_counts().sort_index()
    ax2.bar(atom_counts.index, atom_counts.values, color="#55A868", edgecolor="white", linewidth=0.4)
    ax2.set_xlabel("Number of Atoms")
    ax2.set_ylabel("Count")
    ax2.set_title("Molecule Size Distribution")

    # 3. Elemental composition (mean fractions)
    ax3 = fig.add_subplot(gs[0, 2])
    elem_cols = ["frac_H", "frac_C", "frac_N", "frac_O", "frac_F"]
    elem_means = X[elem_cols].mean()
    elem_labels = ["H", "C", "N", "O", "F"]
    colors = ["#64B5F6", "#A5D6A7", "#CE93D8", "#EF9A9A", "#FFCC80"]
    ax3.bar(elem_labels, elem_means.values, color=colors, edgecolor="white", linewidth=0.4)
    ax3.set_xlabel("Element")
    ax3.set_ylabel("Mean Fraction")
    ax3.set_title("Mean Elemental Composition")

    # 4. Gap vs. num_atoms scatter
    ax4 = fig.add_subplot(gs[1, 0])
    sc = ax4.scatter(X["num_atoms"], y, alpha=0.3, s=8, c=y, cmap="viridis")
    plt.colorbar(sc, ax=ax4, label="Gap (eV)")
    ax4.set_xlabel("Number of Atoms")
    ax4.set_ylabel("HOMO-LUMO Gap (eV)")
    ax4.set_title("Gap vs. Molecule Size")

    # 5. Gap vs. fraction C
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.scatter(X["frac_C"], y, alpha=0.3, s=8, color="#4C72B0")
    ax5.set_xlabel("Carbon Fraction")
    ax5.set_ylabel("HOMO-LUMO Gap (eV)")
    ax5.set_title("Gap vs. Carbon Fraction")

    # 6. Correlation heatmap of top features
    ax6 = fig.add_subplot(gs[1, 2])
    top_features = ["num_atoms", "num_bonds", "frac_C", "frac_N", "frac_O", "avg_degree", "bond_density"]
    corr = X[top_features].corrwith(pd.Series(y, name="gap")).sort_values()
    colors_corr = ["#d73027" if v < 0 else "#1a9850" for v in corr.values]
    ax6.barh(corr.index, corr.values, color=colors_corr)
    ax6.axvline(0, color="black", linewidth=0.8)
    ax6.set_xlabel("Pearson Correlation with Gap")
    ax6.set_title("Feature–Target Correlations")

    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"  EDA plot saved → {save_path}")
    plt.close()


# ── 4. Model Training & Evaluation ───────────────────────────────────────────

def train_and_evaluate(X, y):
    """
    Train Random Forest and Gradient Boosting regressors.
    Returns the best model, scaler, test split, and metrics dict.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    models = {
        "Random Forest": RandomForestRegressor(
            n_estimators=200, max_depth=12, min_samples_leaf=2,
            n_jobs=-1, random_state=42
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200, max_depth=5, learning_rate=0.05,
            subsample=0.8, random_state=42
        ),
    }

    results = {}
    trained = {}

    for name, model in models.items():
        print(f"\n  Training {name}...")
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)

        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2   = r2_score(y_test, y_pred)

        # 5-fold CV on training set
        cv_scores = cross_val_score(model, X_train_sc, y_train,
                                    cv=5, scoring="r2", n_jobs=-1)

        results[name] = {
            "mae": mae, "rmse": rmse, "r2": r2,
            "cv_r2_mean": cv_scores.mean(), "cv_r2_std": cv_scores.std(),
            "y_pred": y_pred,
        }
        trained[name] = model
        print(f"    MAE  = {mae:.4f} eV")
        print(f"    RMSE = {rmse:.4f} eV")
        print(f"    R²   = {r2:.4f}")
        print(f"    CV R²= {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Pick best model by test R²
    best_name = max(results, key=lambda k: results[k]["r2"])
    print(f"\n  Best model: {best_name} (R² = {results[best_name]['r2']:.4f})")

    return trained[best_name], scaler, X_test_sc, y_test, results, best_name


# ── 5. Result Plots ───────────────────────────────────────────────────────────

def plot_results(results, y_test, feature_names, best_model, save_path="model_results.png"):
    """2×2 result figure: parity plots + residuals + feature importance."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Model Evaluation – HOMO-LUMO Gap Prediction", fontsize=15, fontweight="bold")

    colors = {"Random Forest": "#4C72B0", "Gradient Boosting": "#C44E52"}

    for idx, (name, res) in enumerate(results.items()):
        ax_parity = axes[0, idx]
        y_pred = res["y_pred"]

        lo, hi = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
        ax_parity.scatter(y_test, y_pred, alpha=0.35, s=10, color=colors[name])
        ax_parity.plot([lo, hi], [lo, hi], "k--", linewidth=1.2, label="Ideal")
        ax_parity.set_xlabel("True Gap (eV)")
        ax_parity.set_ylabel("Predicted Gap (eV)")
        ax_parity.set_title(
            f"{name}\nMAE={res['mae']:.3f} eV  RMSE={res['rmse']:.3f} eV  R²={res['r2']:.3f}"
        )
        ax_parity.legend(fontsize=9)

    # Residual plot for best model
    best_name = max(results, key=lambda k: results[k]["r2"])
    res_best   = results[best_name]
    residuals  = y_test - res_best["y_pred"]
    ax_res = axes[1, 0]
    ax_res.scatter(res_best["y_pred"], residuals, alpha=0.35, s=10, color=colors[best_name])
    ax_res.axhline(0, color="black", linewidth=1)
    ax_res.set_xlabel("Predicted Gap (eV)")
    ax_res.set_ylabel("Residual (eV)")
    ax_res.set_title(f"Residuals – {best_name}")

    # Feature importance
    ax_fi = axes[1, 1]
    importances = best_model.feature_importances_
    idx_sorted  = np.argsort(importances)[-12:]          # top 12
    ax_fi.barh(
        [feature_names[i] for i in idx_sorted],
        importances[idx_sorted],
        color=colors[best_name], edgecolor="white", linewidth=0.4
    )
    ax_fi.set_xlabel("Feature Importance (Gini)")
    ax_fi.set_title(f"Top Features – {best_name}")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"  Results plot saved → {save_path}")
    plt.close()


# ── 6. Main ───────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  QM9 HOMO-LUMO Gap Prediction")
    print("=" * 60)

    # Step 1 – Load data
    dataset = load_qm9_subset(root="./data", subset_size=5000)

    # Step 2 – Feature extraction
    print("\n[2] Extracting features...")
    X, y = extract_features(dataset)

    # Step 3 – EDA
    print("\n[3] Generating EDA plots...")
    os.makedirs("outputs", exist_ok=True)
    plot_eda(X, y, save_path="outputs/eda_plots.png")

    # Step 4 – Train & evaluate
    print("\n[4] Training models...")
    best_model, scaler, X_test_sc, y_test, results, best_name = train_and_evaluate(X, y)

    # Step 5 – Result plots
    print("\n[5] Generating result plots...")
    plot_results(results, y_test, list(X.columns), best_model,
                 save_path="outputs/model_results.png")

    # Step 6 – Summary table
    print("\n[6] Summary")
    print("-" * 52)
    print(f"{'Model':<22} {'MAE':>7} {'RMSE':>7} {'R²':>7}  {'CV R²':>12}")
    print("-" * 52)
    for name, res in results.items():
        print(f"{name:<22} {res['mae']:>7.4f} {res['rmse']:>7.4f} "
              f"{res['r2']:>7.4f}  {res['cv_r2_mean']:.4f}±{res['cv_r2_std']:.4f}")
    print("-" * 52)
    print(f"\nBest model  : {best_name}")
    print(f"All outputs saved in ./outputs/")
    print("=" * 60)


if __name__ == "__main__":
    main()
