from pathlib import Path

# rendered HTML (asıl tablolar bunun içinde olmalı)
html_path = Path("data/raw/match_22454_rendered.html")

html = html_path.read_text(encoding="utf-8", errors="ignore")

print("✅ file:", html_path)
print("✅ size:", html_path.stat().st_size, "bytes")
print("✅ contains vbw-o-table:", "vbw-o-table" in html)
print("✅ contains <table:", "<table" in html)
print("✅ contains data-team:", "data-team" in html)
