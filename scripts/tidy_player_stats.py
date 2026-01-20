import pandas as pd

IN_FILE = "data/processed/player_stats_all.csv"
OUT_FILE = "data/processed/player_stats_tidy.csv"


def to_num(s):
    return pd.to_numeric(s, errors="coerce")


def pick_col(df, candidates):
    """Return the first column name in df.columns that matches any candidate exactly."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def main():
    df = pd.read_csv(IN_FILE)

    # empty strings NaN
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # --- 1) Columns names normalize (hyphen vs underscore) ---
    df.columns = [c.strip() for c in df.columns]

    # Some of them come with hyphen :
    # total-abs, efficiency-percentage
    df = df.rename(columns={
        "total-abs": "total_abs",
        "efficiency-percentage": "efficiency_pct",
    })

    # --- 2) Find core columns  ---
    col_player_no = pick_col(df, ["player_no"]) or next((c for c in df.columns if "Player No" in c), None)
    col_player_name = pick_col(df, ["player_name"]) or next((c for c in df.columns if "Player Name" in c), None)
    col_pos = pick_col(df, ["position"]) or next((c for c in df.columns if c.startswith("Position")), None)

    # team / set / stat we already have
    col_team = pick_col(df, ["team"])
    col_set = pick_col(df, ["set"])
    col_stat = pick_col(df, ["stat"])

    required = [col_player_no, col_player_name, col_team, col_set, col_stat]
    missing = [c for c in required if c is None]
    if missing:
        raise ValueError(
            f"Eksik core kolonlar var: {missing}. Mevcut kolonlar: {list(df.columns)}"
        )

    
    metric_map_new = {
        "total_abs": "total_abs",
        "attacks": "attack_points",
        "blocks": "block_points",
        "serves": "serve_points",
        "errors": "errors",
        "efficiency_pct": "efficiency_pct",
        "point": "point",
        "attempts": "attempts",
        "total": "total",
        "touches": "touches",
        "successful": "successful",
        "digs": "digs",
    }

    
    metric_map_old = {
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

    
    keep_metrics = []
    rename_metrics = {}

    for src, dst in metric_map_new.items():
        if src in df.columns:
            keep_metrics.append(src)
            rename_metrics[src] = dst

    for src, dst in metric_map_old.items():
        if src in df.columns:
            keep_metrics.append(src)
            rename_metrics[src] = dst

    keep = [col_player_no, col_player_name, col_pos, col_team, col_set, col_stat] + keep_metrics
    out = df[keep].copy()

    # --- 4) Column names normalization ---
    out = out.rename(columns={
        col_player_no: "player_no",
        col_player_name: "player_name",
        col_pos: "position",
        col_team: "team",
        col_set: "set",
        col_stat: "stat",
        **rename_metrics,
    })

    # --- 5) Numeric columns ---
    num_cols = [
        c for c in [
            "total_abs", "attack_points", "block_points", "serve_points", "errors",
            "efficiency_pct", "point", "attempts", "total", "touches", "successful", "digs"
        ]
        if c in out.columns
    ]
    for c in num_cols:
        out[c] = to_num(out[c])

    out["player_no"] = to_num(out["player_no"]).astype("Int64")

    
    out = out.dropna(subset=["player_name", "team", "set", "stat"])

    
    if num_cols:
        out = out[out[num_cols].notna().any(axis=1)]

    out = out.sort_values(["team", "set", "stat", "player_name"], kind="stable")

    out.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"✅ {OUT_FILE} yazıldı | satır: {len(out)} | kolon: {len(out.columns)}")


if __name__ == "__main__":
    main()
