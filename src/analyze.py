
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Paths
BASE = os.path.dirname(os.path.dirname(__file__)) if '__file__' in globals() else os.getcwd()
DATA = os.path.join(BASE, 'data', 'sample_jobs.csv')
OUT = os.path.join(BASE, 'outputs')
os.makedirs(OUT, exist_ok=True)

# 1) Load
df = pd.read_csv(DATA)

# 2) Normalize skills -> explode to tidy
def split_and_clean(s):
    if pd.isna(s): return []
    parts = [p.strip() for p in str(s).split(',') if p.strip()]
    # lower-case normalization for counting, but keep original for display
    return parts

df['skill_list'] = df['skills'].apply(split_and_clean)
exploded = df.explode('skill_list').dropna(subset=['skill_list']).copy()
exploded['skill_norm'] = exploded['skill_list'].str.lower()

# 3) Top skills by city
city_skill_counts = exploded.groupby(['location_city','skill_norm']).size().reset_index(name='count')
# For display, capitalize skill names consistently
city_skill_counts['skill'] = city_skill_counts['skill_norm'].str.title()

def top_n_by_group(pdf, group_col, value_col, n=10):
    out = []
    for key, g in pdf.groupby(group_col):
        top = g.sort_values(value_col, ascending=False).head(n)
        top[group_col] = key
        out.append(top)
    if out:
        return pd.concat(out, ignore_index=True)
    return pd.DataFrame(columns=list(pdf.columns))

top10_city = top_n_by_group(city_skill_counts, 'location_city', 'count', n=10)
top10_city_path = os.path.join(OUT, 'top10_skills_by_city.csv')
top10_city[['location_city','skill','count']].to_csv(top10_city_path, index=False)

# Plot city-wise bar charts in a single tall figure (one figure per city as separate saves)
for city, g in top10_city.groupby('location_city'):
    plt.figure(figsize=(10,6))
    g = g.sort_values('count', ascending=True)
    plt.barh(g['skill'], g['count'])
    plt.title(f"Top 10 Skills in {city}")
    plt.xlabel("Mentions (count)")
    plt.ylabel("Skill")
    plt.tight_layout()
    fig_path = os.path.join(OUT, f"top10_skills_{city}.png")
    plt.savefig(fig_path)
    plt.close()

# 4) Role vs Skill matrix
role_skill = exploded.groupby(['title','skill_norm']).size().unstack(fill_value=0)
# Save matrix as CSV (with title-case skill headers)
role_skill.columns = [c.title() for c in role_skill.columns]
role_skill_path = os.path.join(OUT, 'role_skill_matrix.csv')
role_skill.to_csv(role_skill_path)

# Heatmap
plt.figure(figsize=(12,6))
plt.imshow(role_skill.values, aspect='auto')
plt.xticks(ticks=np.arange(role_skill.shape[1]), labels=role_skill.columns, rotation=90)
plt.yticks(ticks=np.arange(role_skill.shape[0]), labels=role_skill.index)
plt.title("Role vs Skill — Demand Heatmap")
plt.xlabel("Skill")
plt.ylabel("Role")
plt.tight_layout()
heatmap_path = os.path.join(OUT, 'role_skill_heatmap.png')
plt.savefig(heatmap_path)
plt.close()

# 5) Simple recommendations
#    For each city: top 3 skills
rec_lines = []
for city, g in top10_city.groupby('location_city'):
    top3 = g.sort_values('count', ascending=False).head(3)
    s = ", ".join(top3['skill'].tolist())
    rec_lines.append(f"- {city}: Focus on {s}")

#    For each role: top 5 skills unique to role (by ratio vs mean)
role_totals = role_skill.sum(axis=1)
skill_totals = role_skill.sum(axis=0)
role_recs = []
for role in role_skill.index:
    row = role_skill.loc[role]
    # compute a simple "lift": role skill / average across roles (add small epsilon)
    avg = (skill_totals / len(role_skill.index)).replace(0, 0.1)
    lift = (row / avg).sort_values(ascending=False).head(5)
    role_recs.append(f"- {role}: Prioritize " + ", ".join(lift.index.tolist()))

recommendations = ["Job Demand Recommendations",
                   "",
                   "By City:"] + rec_lines + ["", "By Role:"] + role_recs

with open(os.path.join(OUT, "recommendations.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(recommendations))

print("Analysis complete. Outputs saved to:", OUT)
