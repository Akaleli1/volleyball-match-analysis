from pathlib import Path
import csv
from bs4 import BeautifulSoup

# INPUT
HTML_PATH = Path("data/raw/match_22454_rendered.html")

# OUTPUTS
OUT_DIR = Path("data/processed")
TEAM_OUT = OUT_DIR / "team_stats.csv"
PLAYER_OUT = OUT_DIR / "player_stats_all.csv"


def clean_text(x: str) -> str:
    return " ".join((x or "").split()).strip()


def main():
    if not HTML_PATH.exists():
        raise FileNotFoundError(f"Missing HTML file: {HTML_PATH.resolve()}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    html = HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    # 1) Team stats (match header summary area)
    # We keep this simple: find the first "Match Stats" table-ish block by reading the original CSV you already had.
    # If you later want stronger parsing, we can improve it.
    # For now: write team_stats.csv ONLY if found in HTML (optional)
    team_rows = []
    # Try to find text blocks that look like team stats already embedded; fallback: leave empty.
    # (Your previous pipeline already created team_stats.csv; this just standardizes paths.)
    if not TEAM_OUT.exists():
        with TEAM_OUT.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["teamA", "stat", "teamB"])
            # leave blank if not parsed
        print("ℹ️ team_stats.csv created (empty placeholder)")

    # 2) Player stats tables
    tables = soup.select("table.vbw-match-player-statistic-table")
    print(f"Bulunan player tabloları: {len(tables)}")

    # Extract each table as tidy-ish rows (wide columns vary by stat type)
    rows = []
    for table in tables:
        team = table.get("data-team")
        set_ = table.get("data-set")
        stat = table.get("data-stattype")

        # headers
        headers = []
        thead = table.find("thead")
        if thead:
            for th in thead.select("th"):
                cls = " ".join(th.get("class", [])).strip()
                headers.append(cls if cls else clean_text(th.get_text(" ")))

        tbody = table.find("tbody")
        if not tbody:
            continue

        for tr in tbody.select("tr"):
            player_no = tr.get("data-player-no") or ""
            tds = tr.find_all("td")
            vals = [clean_text(td.get_text(" ")) for td in tds]

            # ensure we have at least some structure
            if not vals:
                continue

            row = {
                "player_no": player_no,
                "team": team,
                "set": set_,
                "stat": stat,
            }

            # map by td class when possible (more robust than position index)
            for td in tds:
                cls_list = td.get("class", [])
                if not cls_list:
                    continue
                key = cls_list[-1]  # last class tends to be the semantic one
                text = clean_text(td.get_text(" "))
                if key == "playername":
                    a = td.find("a")
                    row["player_name"] = clean_text(a.get_text(" ")) if a else text
                elif key == "shirtnumber":
                    row["shirt_number"] = text
                else:
                    row[key] = text

            # fallback if player_name missing
            row.setdefault("player_name", "")
            row.setdefault("position", row.get("position", ""))

            rows.append(row)

    # Write player_stats_all.csv (wide)
    # Collect all keys to make a consistent CSV
    all_keys = set()
    for r in rows:
        all_keys.update(r.keys())
    # keep some keys first
    preferred = ["player_no", "shirt_number", "player_name", "position", "team", "set", "stat"]
    fieldnames = preferred + sorted([k for k in all_keys if k not in preferred])

    with PLAYER_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"✅ {PLAYER_OUT.name} yazıldı | satır: {len(rows)}")


if __name__ == "__main__":
    main()
