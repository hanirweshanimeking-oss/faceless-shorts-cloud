import sqlite3
from datetime import datetime

conn = sqlite3.connect('C:/Users/DESKTOP/Downloads/money/DRAGON_HIDDEN_REBIRTH/database/manga_production.db')
c = conn.cursor()

c.execute("UPDATE chapters SET status='EXPORTED' WHERE id='ch_002'")
for p_num in [1, 2, 3]:
    p_id = f"ch_002_p{p_num:02d}"
    c.execute("INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, status, created_at) VALUES (?, 'ch_002', ?, '8_PANEL_DENSE_CINEMATIC', 'QA_PASSED', ?)", (p_id, p_num, datetime.utcnow()))

conn.commit()
print("Database successfully updated for Chapter 2!")
