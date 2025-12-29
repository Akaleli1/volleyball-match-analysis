import pandas as pd

IN_FILE = "player_stats_all.csv"
OUT_FILE = "player_stats_tidy.csv"

def to_num(s):
    return pd.to_numeric(s, errors="coerce")

def main():
    df = pd.read_csv(IN_FILE)

    # Küçük temizlik: boş stringleri NaN yap
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Bazı kolon adları sende böyle geliyor: "Player No No", "Player Name Player" vs.
    # Kolonları güvenli şekilde yakalayalım:
    col_player_no = next((c for c in df.columns if "Player No" in c), None)
    col_player_name = next((c for c in df.columns if "Player Name" in c), None)
    col_pos = next((c for c in df.columns if c.startswith("Position")), None)

    required = [col_player_no, col_player_name, "team", "set", "stat"]
    missing = [c for c in required if c is None or c not in df.columns]
    if missing:
        raise ValueError(f"Eksik kolonlar var: {missing}. Mevcut kolonlar: {list(df.columns)}")

    # Stat türlerine göre kullanılabilecek metric kolonları
    metric_cols = [
        "Total ABS ABS", "Attack Points A Pts", "Block Points B Pts", "Serve Points S Pts",
        "Errors Err", "Efficiency % Eff",
        "Point Pt", "Attempts Att", "Total Tot.",
        "Touches Touches",
        "Successful Successful",
        "Digs Dig",
    ]

    # Sende varsa al, yoksa es geç
    metric_cols = [c for c in metric_cols if c in df.columns]

    keep = [col_player_no, col_player_name, col_pos, "team", "set", "stat"] + metric_cols
    out = df[keep].copy()

    # Kolon isimlerini normalize edelim
    out = out.rename(
        columns={
            col_player_no: "player_no",
            col_player_name: "player_name",
            col_pos: "position",
            "Total ABS ABS": "total_abs",
            "Attack Points A Pts": "attack_points",
            "Block Points B Pts": "block_points",
            "Serve Points S Pts": "serve_points",
            "Errors Err": "errors",
            "Efficiency % Eff": "efficiency_pct",
            "Point Pt": "point",
            "Attempts Att": "attempts",
            "Total Tot.": "total",
            "Touches Touches": "touches",
            "Successful Successful": "successful",
            "Digs Dig": "digs",
        }
    )

    # Sayısal kolonlar
    num_cols = [c for c in ["total_abs","attack_points","block_points","serve_points","errors",
                           "efficiency_pct","point","attempts","total","touches","successful","digs"]
                if c in out.columns]
    for c in num_cols:
        out[c] = to_num(out[c])

    # player_no da num olsun
    out["player_no"] = to_num(out["player_no"]).astype("Int64")

    # Boş satırları temizle: player_name yoksa veya team/set/stat yoksa at
    out = out.dropna(subset=["player_name", "team", "set", "stat"])

    # Stat bazında en az bir metric dolu olmalı (yoksa tamamen boş satırdır)
    if num_cols:
        out = out[out[num_cols].notna().any(axis=1)]

    # Düzen
    out = out.sort_values(["team", "set", "stat", "player_name"], kind="stable")

    out.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"✅ {OUT_FILE} yazıldı | satır: {len(out)} | kolon: {len(out.columns)}")

if __name__ == "__main__":
    main()