import os
import asyncio
import json
from aiokafka import AIOKafkaConsumer
import asyncpg
import time
from datetime import datetime
from typing import List, Dict, Any

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TEMPERATURE_TOPIC = os.getenv("TEMPERATURE_TOPIC", "temperature_reads")
PRICE_TOPIC = os.getenv("PRICE_TOPIC", "price_lookups")
PG_DSN = os.getenv("PG_DSN", "postgresql://rfiduser:rfidpass@postgres:5432/rfiddb")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
BATCH_TIMEOUT = float(os.getenv("BATCH_TIMEOUT", "1"))

# SQL statements
INSERT_TEMPERATURE_SQL = """
    INSERT INTO temperature_reads (event, epc, temperature, unit, timestamp)
    VALUES ($1, $2, $3, $4, $5)
"""

INSERT_PRICE_SQL = """
    INSERT INTO price_lookups (event, epc, item_name, sku, price, currency, timestamp)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
"""

def process_temperature_message(msg_value: bytes) -> tuple:
    obj = json.loads(msg_value)
    
    # Convert timestamp string to datetime object
    timestamp_str = obj.get("timestamp")
    try:
        # Parse ISO format timestamp to datetime object
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except Exception as e:
        print(f"Error parsing timestamp {timestamp_str}: {e}")
        timestamp = datetime.now()
    
    return (
        obj.get("event"),
        obj.get("epc"),
        obj.get("temperature"),
        obj.get("unit"),
        timestamp  # Now passing datetime object instead of string
    )


def process_price_message(msg_value: bytes) -> tuple:
    obj = json.loads(msg_value)
    item_details = obj.get("item_details", {})
    
    # Convert timestamp string to datetime object
    timestamp_str = obj.get("timestamp")
    try:
        # Parse ISO format timestamp to datetime object
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except Exception as e:
        print(f"Error parsing timestamp {timestamp_str}: {e}")
        timestamp = datetime.now()
    
    return (
        obj.get("event"),
        obj.get("epc"),
        item_details.get("name"),
        item_details.get("sku"),
        item_details.get("price"),
        item_details.get("currency"),
        timestamp  # Now passing datetime object instead of string
    )

async def consume_topic(consumer: AIOKafkaConsumer, pool: asyncpg.Pool, topic: str):
    batch = []
    last_flush = time.time()
    is_temperature = topic == TEMPERATURE_TOPIC

    async def flush_batch(to_insert: List[tuple]):
        if not to_insert:
            return
        async with pool.acquire() as conn:
            async with conn.transaction():
                if is_temperature:
                    await conn.executemany(INSERT_TEMPERATURE_SQL, to_insert)
                else:
                    await conn.executemany(INSERT_PRICE_SQL, to_insert)
        print(f"Inserted {len(to_insert)} records into {topic}")

    async for msg in consumer:
        try:
            if is_temperature:
                processed = process_temperature_message(msg.value)
            else:
                processed = process_price_message(msg.value)
            batch.append(processed)
        except Exception as e:
            print(f"Error processing message: {e}")
            continue

        now = time.time()
        if len(batch) >= BATCH_SIZE or (now - last_flush) >= BATCH_TIMEOUT:
            to_write = batch.copy()
            batch.clear()
            last_flush = now
            await flush_batch(to_write)

async def main():
    # Create database connection pool
    pool = await asyncpg.create_pool(dsn=PG_DSN, min_size=5, max_size=20)

    # Create consumers for both topics
    temperature_consumer = AIOKafkaConsumer(
        TEMPERATURE_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="rfid_temperature_ingestor",
        auto_offset_reset="earliest"
    )

    price_consumer = AIOKafkaConsumer(
        PRICE_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="rfid_price_ingestor", 
        auto_offset_reset="earliest"
    )

    await temperature_consumer.start()
    await price_consumer.start()

    try:
        # Consume from both topics concurrently
        await asyncio.gather(
            consume_topic(temperature_consumer, pool, TEMPERATURE_TOPIC),
            consume_topic(price_consumer, pool, PRICE_TOPIC)
        )
    finally:
        await temperature_consumer.stop()
        await price_consumer.stop()
        await pool.close()

if __name__ == "__main__":
    asyncio.run(main())