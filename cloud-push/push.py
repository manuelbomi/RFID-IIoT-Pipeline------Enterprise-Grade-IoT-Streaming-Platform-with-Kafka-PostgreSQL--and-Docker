import os
import asyncio
import asyncpg
import time
import csv
from datetime import datetime

PG_DSN = os.getenv("PG_DSN", "postgresql://user:pass@localhost:5432/db")
PUSH_INTERVAL = int(os.getenv("PUSH_INTERVAL_SECONDS", "30"))
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/data/export")

EXPORT_TEMPERATURE_SQL = """
  SELECT event, epc, temperature, unit, timestamp
  FROM temperature_reads
  WHERE timestamp > $1
  ORDER BY timestamp ASC
  LIMIT 10000
"""

EXPORT_PRICE_SQL = """
  SELECT event, epc, item_name, sku, price, currency, timestamp
  FROM price_lookups
  WHERE timestamp > $1
  ORDER BY timestamp ASC
  LIMIT 10000
"""

async def export_table(conn, sql: str, last_ts: datetime, filename_prefix: str):
    rows = await conn.fetch(sql, last_ts)
    if rows:
        fname = os.path.join(OUTPUT_PATH, f"{filename_prefix}_{int(time.time())}.csv")
        with open(fname, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())  # header
            for rec in rows:
                writer.writerow([rec[k] for k in rec.keys()])
        new_last_ts = rows[-1]["timestamp"]
        print(f"Exported {len(rows)} rows to {fname}")
        return new_last_ts
    return last_ts

async def push_loop():
    pool = await asyncpg.create_pool(dsn=PG_DSN, min_size=2, max_size=5)
    
    # Track last export time for each table
    last_temp_ts = datetime.fromtimestamp(0)
    last_price_ts = datetime.fromtimestamp(0)
    
    while True:
        async with pool.acquire() as conn:
            last_temp_ts = await export_table(conn, EXPORT_TEMPERATURE_SQL, last_temp_ts, "temperature")
            last_price_ts = await export_table(conn, EXPORT_PRICE_SQL, last_price_ts, "price")
        
        await asyncio.sleep(PUSH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(push_loop())