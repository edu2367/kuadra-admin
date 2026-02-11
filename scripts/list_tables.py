import sqlite3
conn = sqlite3.connect('kuadra_reset.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
rows = c.fetchall()
for r in rows:
    print(r[0])
conn.close()
