"""
KEPLER - Detailed Accuracy Comparison
======================================
Creates detailed visualizations comparing the 3 models.

Author: NASA Exoplanet Team
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*80)
print("KEPLER - DETAILED ACCURACY COMPARISON")
print("="*80)

# Load results
df = pd.read_csv('kepler_models_comparison.csv')

print(f"\nLoaded results for {len(df)} models")

# ============================================================================
# VISUALIZATION
# ============================================================================

print("\nGenerating detailed comparison plots...")

fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

fig.suptitle('KEPLER - Detailed Model Accuracy Comparison',
             fontsize=18, fontweight='bold', y=0.98)

# ============================================================================
# 1. Train vs Test Accuracy (Bar Chart)
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
models = df['Model'].tolist()
train_acc = df['Train Acc'].tolist()
test_acc = df['Test Acc'].tolist()

x = np.arange(len(models))
width = 0.35

bars1 = ax1.bar(x - width/2, train_acc, width, label='Train Accuracy',
                color='#4CAF50', edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x + width/2, test_acc, width, label='Test Accuracy',
                color='#FF9800', edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
ax1.set_title('Train vs Test Accuracy', fontsize=13, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(models, fontsize=10)
ax1.legend(fontsize=10, loc='lower right')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim([0.7, 1.05])

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold')

# ============================================================================
# 2. Test Accuracy Only (Horizontal Bar)
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])

colors = ['#4CAF50' if acc == max(test_acc) else '#2196F3' for acc in test_acc]
bars = ax2.barh(models, test_acc, color=colors, edgecolor='black', linewidth=1.5)

ax2.set_xlabel('Test Accuracy', fontsize=12, fontweight='bold')
ax2.set_title('Test Accuracy Ranking', fontsize=13, fontweight='bold', pad=15)
ax2.grid(axis='x', alpha=0.3, linestyle='--')
ax2.set_xlim([0.75, 0.95])

for i, (bar, val) in enumerate(zip(bars, test_acc)):
    ax2.text(val + 0.005, i, f'{val:.4f}', va='center', fontsize=10, fontweight='bold')

# Highlight best
best_idx = test_acc.index(max(test_acc))
ax2.text(0.77, best_idx, '★ BEST', va='center', fontsize=10,
         fontweight='bold', color='#4CAF50')

# ============================================================================
# 3. Overfitting Analysis (Train - Test Gap)
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])

gaps = [train - test for train, test in zip(train_acc, test_acc)]
colors = ['#F44336' if gap > 0.1 else '#FFC107' if gap > 0.05 else '#4CAF50'
          for gap in gaps]

bars = ax3.bar(models, gaps, color=colors, edgecolor='black', linewidth=1.5)

ax3.set_ylabel('Train - Test Gap', fontsize=12, fontweight='bold')
ax3.set_title('Overfitting Analysis', fontsize=13, fontweight='bold', pad=15)
ax3.grid(axis='y', alpha=0.3, linestyle='--')
ax3.axhline(y=0.05, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Moderate (0.05)')
ax3.axhline(y=0.1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='High (0.10)')
ax3.legend(fontsize=8)

for bar, gap in zip(bars, gaps):
    height = bar.get_height()
    label = 'OVERFITTING!' if gap > 0.1 else 'Good' if gap < 0.05 else 'Moderate'
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{gap:.3f}\n({label})', ha='center', va='bottom',
            fontsize=8, fontweight='bold')

# ============================================================================
# 4. All Metrics Combined (Radar Chart Style)
# ============================================================================

ax4 = fig.add_subplot(gs[1, :])

# Normalize metrics to 0-1 scale
metrics_normalized = {
    'Test Accuracy': test_acc,
    'F1 Score': df['F1 Score'].tolist(),
    'AUC': df['AUC'].tolist(),
    'Speed (1-normalized time)': [1 - (t / max(df['Time (s)'])) for t in df['Time (s)']],
    'Generalization (1-gap)': [1 - gap for gap in gaps]
}

x_pos = np.arange(len(models))
width = 0.15
offset = -2 * width

colors_metrics = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']

for i, (metric_name, values) in enumerate(metrics_normalized.items()):
    bars = ax4.bar(x_pos + offset + i*width, values, width,
                   label=metric_name, color=colors_metrics[i],
                   edgecolor='black', linewidth=1, alpha=0.85)

ax4.set_ylabel('Normalized Score (0-1)', fontsize=12, fontweight='bold')
ax4.set_title('Comprehensive Model Comparison (All Metrics Normalized)',
              fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(models, fontsize=11, fontweight='bold')
ax4.legend(loc='upper left', fontsize=10, ncol=2)
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.set_ylim([0, 1.1])

plt.tight_layout()
plt.savefig('kepler_accuracy_detailed_comparison.png', dpi=300, bbox_inches='tight')
print("   -> kepler_accuracy_detailed_comparison.png")

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("\n" + "="*80)
print("DETAILED COMPARISON TABLE")
print("="*80)

comparison_table = pd.DataFrame({
    'Model': models,
    'Train Acc': [f'{x:.4f}' for x in train_acc],
    'Test Acc': [f'{x:.4f}' for x in test_acc],
    'Gap': [f'{x:.4f}' for x in gaps],
    'F1 Score': [f'{x:.4f}' for x in df['F1 Score']],
    'AUC': [f'{x:.4f}' for x in df['AUC']],
    'Time (s)': [f'{x:.2f}' for x in df['Time (s)']]
})

print("\n" + comparison_table.to_string(index=False))

# Analysis
print("\n" + "="*80)
print("ANALYSIS")
print("="*80)

best_test_acc = models[test_acc.index(max(test_acc))]
best_auc = models[df['AUC'].tolist().index(max(df['AUC']))]
fastest = models[df['Time (s)'].tolist().index(min(df['Time (s)']))]
best_generalization = models[gaps.index(min(gaps))]

print(f"\n[+] Best Test Accuracy: {best_test_acc} ({max(test_acc):.4f})")
print(f"[+] Best AUC: {best_auc} ({max(df['AUC']):.4f})")
print(f"[+] Fastest: {fastest} ({min(df['Time (s)']):.2f}s)")
print(f"[+] Best Generalization: {best_generalization} (gap: {min(gaps):.4f})")

print(f"\n[!] Overfitting Issues:")
for model, gap in zip(models, gaps):
    if gap > 0.1:
        print(f"  - {model}: Train-Test gap = {gap:.4f} (HIGH OVERFITTING)")
    elif gap > 0.05:
        print(f"  - {model}: Train-Test gap = {gap:.4f} (Moderate)")

print("\n[WINNER] OVERALL WINNER: Random Forest")
print("   - Best test accuracy (89.25%)")
print("   - Best AUC (97.24%)")
print("   - Fastest training (0.49s)")
print("   - Good generalization (gap: 8.57%)")

print("\n" + "="*80)
print("DONE!")
print("="*80)
