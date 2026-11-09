import sqlite3
import json

db_path = r'c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH\database\manga_production.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in c.fetchall()]
print("Tables:", tables)

for t in tables:
    c.execute(f"SELECT count(*) FROM {t}")
    cnt = c.fetchone()[0]
    print(f"\n--- {t} ({cnt} rows) ---")
    if cnt > 0:
        c.execute(f"SELECT * FROM {t} LIMIT 3")
        cols = [d[0] for d in c.description]
        for row in c.fetchall():
            row_dict = dict(zip(cols, row))
            print(json.dumps({k: v for k, v in row_dict.items() if v is not None}, indent=2)[:300])
