
# Job Trend Analysis (Ethical Web Data)

**Objective:** Skills ki demand ko cities aur roles ke hisaab se analyse karna (Top 10 skills by city + Role–Skill matrix + Recommendations).

> ⚠️ **Important (Legal & Ethical):** LinkedIn ya kisi bhi website ko bina permission scrape karna Terms of Service ka violation ho sakta hai. Is project mein hum **public/ethical sources** (API/datasets) ya provided **sample data** use karte hain. Aap live data ke liye Adzuna API, JSearch API (RapidAPI), Greenhouse/Lever careers pages, ya sarkari/official job boards (e.g., USAJOBS) jaisi jagahon ka istemaal karein jahan terms allow karte hain.

## Project Structure
```
job-trend-analysis-project/
  ├── data/
  │   └── sample_jobs.csv
  ├── outputs/               # yahan charts & CSV generate honge
  ├── src/
  │   └── analyze.py         # main analysis script
  ├── README.md
  └── requirements.txt
```

## Quick Start
1. **Python 3.9+** install hona chahiye.
2. Dependencies install karein:
   ```bash
   pip install -r requirements.txt
   ```
3. Analysis run karein:
   ```bash
   python src/analyze.py
   ```
4. Results `outputs/` folder me milenge:
   - `top10_skills_<CITY>.png`
   - `top10_skills_by_city.csv`
   - `role_skill_matrix.csv`
   - `role_skill_heatmap.png`
   - `recommendations.txt`

## Data Source Options (LinkedIn Alternative)
- **Adzuna API** (global jobs), **JSearch API** (RapidAPI), **Greenhouse/Lever** public careers pages
- **Public datasets** (e.g., Kaggle par posted job postings datasets)
- **Official boards** (e.g., USAJOBS, EU public sectors) – terms allow programmatic access

> Aap `data/` me `sample_jobs.csv` ko apne real data se replace kar sakte hain (same columns rakhein).

## What This Project Delivers
- **Trend Analysis Visuals:** City-wise Top 10 skills bar charts
- **Skill vs Role Matrix:** CSV + Heatmap
- **Recommendations:** City & Role ke hisaab se focus skills

## Report (1–2 Pages) – Template Points
- **Introduction:** Aim – job market skill-demand trends
- **Tools:** Python (Pandas, NumPy, Matplotlib)
- **Steps:** Data ingest → Clean/parse skills → Aggregations → Visuals → Insights
- **Conclusion:** Top in-demand skills by city/role; training & hiring recommendations

## Customization Tips
- Skill parsing ko aap keyword dictionary se enhance kar sakte hain.
- City/Role filters add karke interactive dashboard (Streamlit) bana sakte hain.
- Time-based trends (weekly/monthly) nikalne ke liye `posted_date` use karein.
