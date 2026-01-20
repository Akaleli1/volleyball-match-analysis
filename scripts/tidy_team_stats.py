import pandas as pd
from pathlib import Path

IN_FILE = Path("data/processed/team_stats.csv")
OUT_FILE = Path("data/processed/team_stats_tidy.csv")

# Bu match sayfasında beklediğimiz takım-stat listesi
KEEP_STATS = {"Attack", "Block", "Serve", "Opponent Error", "Total", "Dig", "Reception", "Set"}

def main():
    df = pd.read_csv(IN_FILE)

    # ÖNEMLİ: Doğru kolonlar -> [Turkey value, stat name, Italy value] = [1,2,3]
    df3 = df.iloc[:, [1, 2, 3]].copy()
    df3.columns = ["teamA", "stat", "teamB"]

    # Stat olmayan satırları ayıkla (Match Skills, Best Scorers vs)
    df3 = df3[df3["stat"].notna()].copy()
    df3["stat"] = df3["stat"].astype(str).str.strip()

    # Sadece takım istatistiklerini tut
    df3 = df3[df3["stat"].isin(KEEP_STATS)].copy()

    # Sayısal kolonları düzelt
    df3["teamA"] = pd.to_numeric(df3["teamA"], errors="coerce")
    df3["teamB"] = pd.to_numeric(df3["teamB"], errors="coerce")
    df3 = df3.dropna(subset=["teamA", "teamB"])

    out = pd.concat([
        df3[["stat", "teamA"]].rename(columns={"teamA": "value"}).assign(team="TUR"),
        df3[["stat", "teamB"]].rename(columns={"teamB": "value"}).assign(team="ITA"),
    ], ignore_index=True)

    out = out[["team", "stat", "value"]]
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_FILE, index=False, encoding="utf-8")

    print(f"✅ team_stats_tidy.csv yazıldı | satır: {len(out)}")

if __name__ == "__main__":
    main()
