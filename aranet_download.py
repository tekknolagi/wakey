#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
import os
import sqlite3
import time
import aranet4

NUM_RETRIES = 10
DEVICES = {
    'kitchen': 'F2:F4:A9:AC:7E:6E',
}

db_path = os.path.join(os.path.expanduser('~/www/'), 'aranet4.db')

con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS measurements(
  device TEXT,
  timestamp INTEGER,
  temperature REAL,
  humidity INTEGER,
  pressure REAL,
  CO2 INTEGER,
  PRIMARY KEY(device, timestamp)
)''')
con.commit()

def timestamp_to_boston(timestamp):
    return datetime.fromtimestamp(timestamp, timezone(timedelta(hours=-8)))

for name, mac in DEVICES.items():
    entry_filter = {}

    res = cur.execute('''SELECT timestamp FROM measurements WHERE device = ?
                         ORDER BY timestamp DESC LIMIT 1''', (name,))
    row = res.fetchone()
    if row is not None:
        entry_filter['start'] = timestamp_to_boston(row[0])

    for attempt in range(NUM_RETRIES):
        entry_filter['end'] = datetime.now()
        try:
            history = aranet4.client.get_all_records(mac, entry_filter)
            break
        except Exception as e:
            print('attempt', attempt, 'failed, retrying:', e)

    data = []
    for entry in history.value:
        if entry.co2 < 0:
            continue

        data.append((
            name,
            entry.date.timestamp(),
            entry.temperature,
            entry.humidity,
            entry.pressure,
            entry.co2
            ))
    print('fetched', len(data), 'measurements', entry_filter)
    cur.executemany(
            'INSERT OR IGNORE INTO measurements VALUES(?, ?, ?, ?, ?, ?)', data)
    con.commit()

con.close()
