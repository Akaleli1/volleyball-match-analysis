from pathlib import Path
import pandas as pd

# ---- Paths (repo root'a göre) ----
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PLAYER_TIDY = PROCESSED_DIR / "player_stats_tidy.csv"
TEAM_TIDY = PROCESSED_DIR / "team_stats_tidy.csv"

OUT_TOP_SCORERS = OUT_DIR / "top_scorers.csv"
OUT_TEAM_SET_SUMMARY = OUT_DIR / "team_set_summary.csv"
OUT_ATTACK_EFF_TOP = OUT_DIR / "attack_eff_top.csv"



def safe_read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise SystemExit(
            f"❌ Bulunamadı: {path}. Önce ilgili scripti çalıştırıp dosyayı üret.\n"
            f"   (Kontrol: {path.resolve()})"
        )


def main():
    # --- Load ---
    df = safe_read_csv(PLAYER_TIDY)

    # Normalize column names (defensive)
    df.columns = [c.strip() for c in df.columns]

    expected_cols = {
        "team", "set", "stat",
        "player_no", "player_name", "position",
        "total_abs", "attack_points", "block_points", "serve_points",
        "errors", "efficiency_pct",
        "point", "attempts", "total",
        "touches", "successful", "digs"
    }
    missing = sorted(list(expected_cols - set(df.columns)))
    if missing:
        print("⚠️ Eksik kolonlar var (bazıları opsiyonel olabilir):", missing)

    # Cast numerics safely
    num_cols = [
        "player_no",
        "total_abs", "attack_points", "block_points", "serve_points",
        "errors", "efficiency_pct",
        "point", "attempts", "total",
        "touches", "successful", "digs"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- 1) TOP SCORERS (All sets scoring table) ---
    scoring_all = df[df["stat"] == "scoring"].copy()

    top_scorers = (
        scoring_all
        .groupby(["team", "player_no", "player_name", "position"], as_index=False)
        .agg(
            points=("total_abs", "max"),
            attack_pts=("attack_points", "max"),
            block_pts=("block_points", "max"),
            serve_pts=("serve_points", "max"),
        )
        .sort_values(["points", "attack_pts"], ascending=[False, False])
    )

    top_scorers.to_csv(OUT_TOP_SCORERS, index=False, encoding="utf-8")
    print(f"✅ {OUT_TOP_SCORERS} yazıldı | satır: {len(top_scorers)}")

    # --- 2) TEAM SET SUMMARY ---
    scoring_all_sets = df[df["stat"] == "scoring"].copy()
    attack_all_sets = df[df["stat"] == "attack"].copy()

    team_set_scoring = (
        scoring_all_sets
        .groupby(["team", "set"], as_index=False)
        .agg(
            total_abs=("total_abs", "sum"),
            attack_pts=("attack_points", "sum"),
            block_pts=("block_points", "sum"),
            serve_pts=("serve_points", "sum"),
        )
    )

    team_set_errors = (
        attack_all_sets
        .groupby(["team", "set"], as_index=False)
        .agg(errors=("errors", "sum"))
    )

    team_set_summary = (
        team_set_scoring
        .merge(team_set_errors, on=["team", "set"], how="left")
        .fillna({"errors": 0})
        .sort_values(["set", "team"])
    )

    team_set_summary.to_csv(OUT_TEAM_SET_SUMMARY, index=False, encoding="utf-8")
    print(f"✅ {OUT_TEAM_SET_SUMMARY} yazıldı | satır: {len(team_set_summary)}")

    # --- 3) ATTACK EFFICIENCY TOP (All sets, attack table) ---
    attack_all = df[(df["stat"] == "attack") & (df["set"] == "all")].copy()

    if "attempts" in attack_all.columns:
        attack_all = attack_all[attack_all["attempts"].fillna(0) > 0]

    attack_eff_top = attack_all[[
        "team", "player_no", "player_name", "position",
        "efficiency_pct", "point", "attempts", "total", "errors"
    ]].copy()

    attack_eff_top = attack_eff_top.dropna(subset=["efficiency_pct"])

    attack_eff_top = attack_eff_top.sort_values(
        ["efficiency_pct", "point", "attempts"],
        ascending=[False, False, False]
    ).head(50)

    attack_eff_top.to_csv(OUT_ATTACK_EFF_TOP, index=False, encoding="utf-8")
    print("✅ attack_eff_top.csv yazıldı | top50")

    # --- 4) Quick check: team_stats_tidy exists? ---
    if TEAM_TIDY.exists():
        tdf = pd.read_csv(TEAM_TIDY)
        print(f"ℹ️ {TEAM_TIDY} OK | satır: {len(tdf)}")
    else:
        print(f"⚠️ {TEAM_TIDY} yok. (Opsiyonel) team tidy üretmediysen sorun değil.")


if __name__ == "__main__":
    main()
