from pathlib import Path

html = Path("match_22454_finished.html").read_text(encoding="utf-8")

print("Contains <table:", "<table" in html)
print("Contains vbw-o-table:", "vbw-o-table" in html)
print("Contains data-team:", "data-team" in html)