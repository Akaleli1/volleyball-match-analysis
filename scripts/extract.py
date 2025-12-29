from bs4 import BeautifulSoup
import pandas as pd

HTML_PATH = "match_22454_rendered.html"

def table_to_df(table):
    header_cells = table.select("thead th")
    headers = [h.get_text(" ", strip=True) for h in header_cells]

    rows = []
    for tr in table.select("tbody tr"):
        cells = tr.select("td")
        if not cells:
            continue
        rows.append([c.get_text(" ", strip=True) for c in cells])

    max_len = max((len(r) for r in rows), default=0)
    if max_len == 0:
        return pd.DataFrame()

    if len(headers) != max_len:
        headers = headers[:max_len] + [f"col_{i}" for i in range(len(headers), max_len)]

    return pd.DataFrame(rows, columns=headers)

def main():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    # 1) Team stats
    team_stats_table = soup.select_one("table.vbw-match-team-statistics-table")
    if team_stats_table:
        df_team = table_to_df(team_stats_table)
        df_team.to_csv("team_stats.csv", index=False, encoding="utf-8")
        print("✅ team_stats.csv yazıldı")
    else:
        print("❌ Team stats tablosu bulunamadı: table.vbw-match-team-statistics-table")

    # 2) Player stats (tüm tablolar)
    player_tables = soup.select("table.vbw-match-player-statistic-table")
    print(f"Bulunan player tabloları: {len(player_tables)}")

    out = []
    for t in player_tables:
        df = table_to_df(t)
        if df.empty:
            continue
        df["team"] = t.get("data-team")      # teama / teamb
        df["set"] = t.get("data-set")        # all / 1 / 2 / ...
        df["stat"] = t.get("data-stattype")  # scoring / attack / block / ...
        out.append(df)

    if out:
        df_all = pd.concat(out, ignore_index=True)
        df_all.to_csv("player_stats_all.csv", index=False, encoding="utf-8")
        print("✅ player_stats_all.csv yazıldı")
    else:
        print("❌ Player stats tabloları parse edilemedi (tablo var ama satır çıkmadı)")

if __name__ == "__main__":
    main()

