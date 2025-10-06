#!/usr/bin/env python3
"""
Plots model performance metrics from a CSV file.

The script reads a CSV file with columns:
  model, train_accuracy, test_accuracy, cv_mean, cv_std, overfit_gap

It then generates a bar chart comparing model accuracies with
cross-validation error bars.

Usage:
    python3 plot_model_performance.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_performance(csv_path: str, save_path: str = "model_performance.png") -> None:
    """
    Plots train, test, and CV mean accuracies from a CSV file.

    Args:
        csv_path (str): Path to the input CSV file.
        save_path (str): Output path for the saved image.
    """
    # Load data
    df = pd.read_csv(csv_path)

    # Extract model names and metrics
    models = df.iloc[:, 0].values
    train_acc = df["train_accuracy"].values
    test_acc = df["test_accuracy"].values
    cv_mean = df["cv_mean"].values
    cv_std = df["cv_std"].values

    # Create x positions
    x = np.arange(len(models))
    width = 0.25

    # Plot bars
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width, train_acc, width, label="Train Accuracy")
    ax.bar(x, test_acc, width, label="Test Accuracy")
    ax.bar(x + width, cv_mean, width, yerr=cv_std, capsize=5,
           label="CV Mean ± Std", alpha=0.8)

    # Labels and formatting
    ax.set_ylabel("Accuracy")
    ax.set_title("Model Performance Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=20)
    ax.set_ylim(0.85, 1.0)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Annotate overfit gap
    for i, gap in enumerate(df["overfit_gap"]):
        ax.text(x[i], test_acc[i] + 0.005, f"Δ={gap:.3f}", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"✅ Saved performance plot as: {save_path}")


if __name__ == "__main__":
    temp_csv = "kepler\model_comparison.csv"
    plot_performance(temp_csv, "kepler\model_performance.png")
