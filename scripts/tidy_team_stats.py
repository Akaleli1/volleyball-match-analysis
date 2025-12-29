import pandas as pd

# team_stats.csv yapısı: col1=teamA sayı, col2=stat, col3=teamB sayı
df = pd.read_csv("team_stats.csv")

# Güvenli şekilde 2.,3.,4. kolonları al (0-index: 1,2,3)
df3 = df.iloc[:, 1:4].copy()
df3.columns = ["teamA", "stat", "teamB"]

# İstediğimiz takım statları (Best Scorers vs. dışarıda kalsın)
wanted = {"Attack", "Block", "Serve", "Opponent Error", "Total", "Dig", "Reception", "Set"}
df3 = df3[df3["stat"].isin(wanted)]

df3["teamA"] = pd.to_numeric(df3["teamA"], errors="coerce")
df3["teamB"] = pd.to_numeric(df3["teamB"], errors="coerce")
df3 = df3.dropna(subset=["teamA", "teamB"])

out = pd.concat(
    [
        df3[["stat", "teamA"]].rename(columns={"teamA": "value"}).assign(team="TUR"),
        df3[["stat", "teamB"]].rename(columns={"teamB": "value"}).assign(team="ITA"),
    ],
    ignore_index=True,
)

out = out[["team", "stat", "value"]]
out.to_csv("team_stats_tidy.csv", index=False, encoding="utf-8")
print("✅ team_stats_tidy.csv yazıldı")
