"""Figure 1: landings per 1,000 with the setting wrong, by class and region, corrected measure. Run from the paper folder."""
import json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = json.load(open('results/after_review.json'))['rates_per1000']
groups = [('air|EU', 'Airline jets\nEurope'), ('air|US', 'Airline jets\nUnited States'), ('biz|EU', 'Business jets\nEurope'), ('biz|US', 'Business jets\nUnited States')]
fig, ax = plt.subplots(figsize=(6.4, 3.3)); w = 0.27
for j, (k, lab, col) in enumerate([('y', '2 hPa or more', '#bdbdbd'), ('y5', '5 hPa or more', '#6b8fb5'), ('y10', '10 hPa or more', '#1f4e79')]):
    vals = [d[g][k][2] for g, _ in groups]
    bars = ax.bar([i + (j - 1) * w for i in range(4)], vals, w, color=col, label=lab)
    for b in bars: ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.12, f'{b.get_height():.2f}', ha='center', fontsize=7)
ax.set_xticks(range(4)); ax.set_xticklabels([g for _, g in groups], fontsize=8); ax.set_ylabel('Landings per 1,000', fontsize=9)
ax.spines[['top', 'right']].set_visible(False); ax.legend(frameon=False, fontsize=8, loc='upper left')
fig.tight_layout(); fig.savefig('figures/rates.pdf')
