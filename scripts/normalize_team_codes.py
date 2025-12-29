import pandas as pd

TEAM_MAP = {"teama": "TUR", "teamb": "ITA"}

def main():
    df = pd.read_csv("player_stats_tidy.csv")
    df["team"] = df["team"].map(TEAM_MAP).fillna(df["team"])
    df.to_csv("player_stats_tidy.csv", index=False, encoding="utf-8")
    print("✅ player_stats_tidy.csv içinde team kodları normalize edildi (TUR/ITA).")

if __name__ == "__main__":
    main()
