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



# ## High level code explanation 
# This is a high-performance, batched stream ingestor that consumes IoT events from Kafka and persists them to a PostgreSQL database using optimized batch operations.

# ## Architecture & Design Patterns:

# Dual-Topic Consumption: It runs two independent Kafka consumers in parallel (asyncio.gather) for temperature and price topics, maintaining separation of concerns and allowing each stream to be processed at its own rate.

# Batch Processing for High Throughput:

# Size-Based Batching: Uses BATCH_SIZE (default: 1000) to accumulate messages until reaching an optimal bulk insert size

# Time-Based Batching: Uses BATCH_TIMEOUT (default: 1 second) as a fallback to ensure data isn't delayed too long during low-throughput periods

# This batching dramatically reduces database round-trips and improves I/O efficiency


# ### Database Optimization:

# Connection Pooling: Uses asyncpg.Pool with 5-20 connections to handle concurrent database operations efficiently

# Bulk Inserts: Uses executemany() for batched SQL execution, which is significantly faster than individual inserts

# Transaction Management: Wraps each batch in a transaction for atomicity and performance


# ### Data Processing Pipeline:

# text
# Kafka Message → JSON Parsing → Timestamp Conversion → Batch Accumulation → Bulk Database Insert
# The timestamp conversion from ISO format to PostgreSQL-native datetime objects is crucial for proper time-series querying

# Error handling at each stage prevents single bad messages from breaking the entire pipeline


# ## Scalability Features:

# Consumer Groups: Each consumer uses a different group_id, allowing for horizontal scaling - you could run multiple instances of this service

# Asynchronous I/O: Uses asyncpg and aiokafka for non-blocking database and Kafka operations

# Configurable Parameters: All key parameters (batch size, timeout, connection settings) are environment-configurable


# ##Why This Matters for IoT:
# In real IoT deployments with thousands of devices generating data continuously, this batched approach is essential for:

# Handling data spikes without overwhelming the database

# Reducing storage latency while maintaining throughput

# Cost efficiency through optimal resource utilization

# Reliable data persistence with proper error handling

# This consumer represents the "T" in ETL - it's responsible for efficiently loading streaming IoT data into a structured storage system where it can be queried, analyzed, and visualized.
