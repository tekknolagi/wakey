#!/usr/bin/env python3
import os
import sqlite3
import json
db_path = os.path.join(os.path.expanduser('~/www/'), 'aranet4.db')
con = sqlite3.connect(db_path)
cur = con.cursor()
res = cur.execute("""
    SELECT * FROM (
        SELECT device, timestamp, CO2
        FROM measurements
        ORDER BY timestamp DESC
        LIMIT 100
    ) ORDER BY timestamp ASC
""")
rows = [{"device": r[0], "timestamp": str(r[1]), "CO2": r[2]} for r in res.fetchall()]
print("Content-Type: application/json")
print()
print(json.dumps(rows))
con.close()
