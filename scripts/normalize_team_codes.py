import pandas as pd

IN_FILE = "data/processed/player_stats_tidy.csv"
OUT_FILE = "data/processed/player_stats_tidy.csv"  # same file, overwrite

TEAM_MAP = {
    "teama": "TUR",
    "teamb": "ITA",
}

def main():
    df = pd.read_csv(IN_FILE)

    if "team" not in df.columns:
        raise SystemExit("❌ 'team' kolonu yok. player_stats_tidy.csv formatı beklenenden farklı.")

    df["team"] = df["team"].astype(str).str.strip().str.lower().map(TEAM_MAP).fillna(df["team"])

    df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"✅ team codes normalized -> {OUT_FILE}")

if __name__ == "__main__":
    main()
