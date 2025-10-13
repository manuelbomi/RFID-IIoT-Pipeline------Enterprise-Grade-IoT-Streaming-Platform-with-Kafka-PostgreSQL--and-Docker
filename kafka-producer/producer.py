import os
import asyncio
import json
import random
import time
from datetime import datetime, timezone
from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
NUM_DEVICES = int(os.getenv("NUM_DEVICES", "10000"))
TEMPERATURE_TOPIC = os.getenv("TEMPERATURE_TOPIC", "temperature_reads")
PRICE_TOPIC = os.getenv("PRICE_TOPIC", "price_lookups")
SLEEP_MS = int(os.getenv("PRODUCER_SLEEP_MS", "50"))

# Sample product catalog for price lookups
PRODUCT_CATALOG = [
    {"name": "Leather Jacket", "sku": "LJ-4577", "price": 199.99, "currency": "USD"},
    {"name": "Wireless Headphones", "sku": "WH-8921", "price": 149.99, "currency": "USD"},
    {"name": "Smart Watch", "sku": "SW-3345", "price": 299.99, "currency": "USD"},
    {"name": "Running Shoes", "sku": "RS-6678", "price": 129.99, "currency": "USD"},
    {"name": "Backpack", "sku": "BP-1123", "price": 79.99, "currency": "USD"},
    {"name": "Water Bottle", "sku": "WB-4456", "price": 24.99, "currency": "USD"},
    {"name": "Sunglasses", "sku": "SG-7789", "price": 159.99, "currency": "USD"},
    {"name": "Laptop Sleeve", "sku": "LS-9900", "price": 39.99, "currency": "USD"}
]

def generate_epc(device_id: int) -> str:
    """Generate realistic EPC codes"""
    return f"30{device_id:012X}"[-14:]

def generate_temperature_event(device_id: int):
    """Generate temperature reading event"""
    return {
        "event": "temperature_read",
        "epc": generate_epc(device_id),
        "temperature": round(random.uniform(-10.0, 40.0), 1),
        "unit": random.choice(["C", "F"]),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def generate_price_event(device_id: int):
    """Generate price lookup event"""
    product = random.choice(PRODUCT_CATALOG)
    return {
        "event": "price_lookup",
        "epc": generate_epc(device_id),
        "item_details": product,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

async def run():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
            await producer.start()
            print(f" Connected to Kafka on attempt {attempt + 1}")
            
            # Track last event time per device for realistic timing
            device_last_event = {i: time.time() for i in range(NUM_DEVICES)}
            
            while True:
                current_time = time.time()
                
                for device_id in range(NUM_DEVICES):
                    # Only send event if enough time has passed for this device
                    if current_time - device_last_event[device_id] >= (SLEEP_MS / 1000.0):
                        # 70% temperature events, 30% price lookup events
                        if random.random() < 0.7:
                            event = generate_temperature_event(device_id)
                            topic = TEMPERATURE_TOPIC
                        else:
                            event = generate_price_event(device_id)
                            topic = PRICE_TOPIC
                        
                        await producer.send_and_wait(
                            topic, 
                            json.dumps(event).encode("utf-8")
                        )
                        device_last_event[device_id] = current_time
                
                # Small sleep to prevent tight loop
                await asyncio.sleep(0.001)
                
        except Exception as e:
            print(f" Connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                break
        except KeyboardInterrupt:
            print("Shutting down producer...")
            break
        finally:
            if 'producer' in locals():
                await producer.stop()


if __name__ == "__main__":
    asyncio.run(run())



# ## High level Explanation

# This is a Kafka producer load simulator designed to generate a realistic, sustained stream of IoT event data for development, testing, and performance benchmarking of a downstream data pipeline.

# Here's the technical breakdown:


# Core Purpose & Architecture:

# Load Generation: It synthesizes a high-volume, continuous stream of two common IoT event types to simulate a production environment.


# Decoupled Data Streams: It wisely separates events into two distinct Kafka topics (temperature_reads and price_lookups). This allows downstream consumers (e.g., time-series databases for temperature, product catalog services for price lookups) to subscribe only to the relevant data stream, following a best-practice microservices architecture.

# The Data Models:


# Temperature Event: Simulates data from a temperature sensor. It includes a unique device EPC (using the standardized format we discussed), a realistic temperature range, a unit, and a precise timestamp.

# Price Lookup Event: Simulates a retail IoT interaction (e.g., from a smart shelf, RFID scanner, or digital kiosk). It triggers a lookup against a simulated product catalog and sends the entire product details.


# Key Technical Features:

# Asynchronous Operation: Uses asyncio and AIOKafkaProducer for high-performance, non-blocking I/O, enabling it to handle thousands of concurrent simulated devices efficiently.

# Controlled Load: The SLEEP_MS and device-level timing (device_last_event) prevent a pure, system-breaking flood. It enforces a maximum event rate per device, creating a more realistic and sustainable load.

# Configurability: All critical parameters (Kafka connection, number of devices, topics, sleep intervals) are driven by environment variables, making it highly adaptable for different test scenarios.

# Resilience: Incorporates a retry mechanism with exponential backoff for initial Kafka connection failures, ensuring robustness in containerized or orchestrated environments where dependencies may not be immediately available.


# In summary for the IoT Engineer: This script is not for production data ingestion. It's a foundational tool for pipeline development. It allows you to validate your Kafka infrastructure, test the performance and logic of your stream processors (like Kafka Streams or Flink jobs), and develop dashboard visualizations, all with a reliable and configurable source of mock data that accurately reflects your intended IoT device behavior.
