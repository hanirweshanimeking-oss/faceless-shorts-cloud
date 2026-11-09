import os
from pathlib import Path

root = Path(r"c:\Users\DESKTOP\Downloads\money")
keywords = ["siddhartha", "ike dragon", "jackal", "devraj", "orphanage", "hyderabad", "memory reclamation", "10,000 iq", "10000 iq"]

matches = []
for p in root.rglob("*"):
    if p.is_file() and p.suffix in [".md", ".txt", ".json", ".py", ".sql"]:
        # skip git and venv
        if ".git" in str(p) or "node_modules" in str(p):
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore").lower()
            found = [k for k in keywords if k in content]
            if found:
                matches.append((str(p), found))
        except Exception:
            pass

print(f"Found {len(matches)} files matching canon keywords:")
for path, found in matches[:20]:
    print(f"  {path} -> {found}")
