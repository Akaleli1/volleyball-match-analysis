# Volleyball Match Analytics (WIP)

This project explores **women’s volleyball match and player statistics** using a structured data pipeline built in Python.

The goal is to extract, normalize, and analyze **team- and player-level performance across sets**, enabling deeper analytical questions such as:

- How attack efficiency changes set by set
- Which players maintain performance consistency
- How teams perform in long (5-set) matches
- Error distribution across teams and sets

> ⚠️ This repository currently contains **analysis code only**.  
> Raw match data and generated outputs are intentionally excluded.

---

## 📁 Project Structure

```text
wbw_scraper/
├── scripts/
│   ├── extract.py                # Extract raw stats from rendered HTML
│   ├── tidy_player_stats.py      # Normalize player-level statistics
│   ├── tidy_team_stats.py        # Normalize team-level statistics
│   ├── normalize_team_codes.py   # Map internal team codes to readable names
│   ├── summary_report.py         # Generate analytical summaries
│   └── smoke_test.py             # Lightweight sanity checks
├── .gitignore
└── README.md
```

## 🔍 What This Project Does
Data Pipeline Overview
1. Extract

- Parses rendered HTML match pages

- Collects team and player statistics across all sets

2. Normalize

- Converts wide / inconsistent tables into tidy datasets

- Standardizes team codes and stat labels

3. Analyze

- Produces summaries such as:

    - Top scorers

    - Team performance per set

    - Attack efficiency rankings

## 📊 Example Analyses (Generated Locally)

- Top scorers by total points

- Team performance by set (attack / block / serve / errors)

- Attack efficiency leaders

- Outputs (CSV files, plots) are generated locally and not committed to the repository.


## 🧪 Reproducibility

- This project is designed to be reproducible without committing raw data.

```Typical workflow
python scripts/extract.py
python scripts/tidy_team_stats.py
python scripts/tidy_player_stats.py
python scripts/summary_report.py
```

## 🚧 Project Status

-  ✅ Core extraction & normalization pipeline

-  ✅ Analytical summaries

- 🚧 Visualization & reporting (planned)

- 🚧 Larger multi-match datasets (planned)

## ⚖️ Notes on Data Usage

- No proprietary or scraped raw data is included

- This repository focuses on code, methodology, and analysis logic

- Sample or synthetic datasets may be added later for demonstration

## 👤 Author

Built by Alaz Kalelioglu
Software Engineer | Data & Analytics | Python