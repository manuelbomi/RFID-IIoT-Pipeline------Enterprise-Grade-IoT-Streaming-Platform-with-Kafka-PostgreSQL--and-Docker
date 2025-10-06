# RFID-IIoT-Pipeline: Enterprise-Grade-IoT-Streaming-Platform-with-Kafka-PostgreSQL-Docker

![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?logo=docker)         ![Apache Kafka](https://img.shields.io/badge/Apache--Kafka-orange.svg?logo=apachekafka)        ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg?logo=postgresql)          ![Python](https://img.shields.io/badge/Python-3.11-green.svg?logo=python)   
         
             
                   


##### The RFID IIoT Pipeline is a comprehensive, production-ready data streaming platform designed specifically for massive-scale IoT and Industrial IoT (IIoT) applications. 

![Image](https://github.com/user-attachments/assets/65f74fd5-6dc3-40b0-b511-13a059f82342)


##### This solution enables enterprises to process, analyze, and manage real-time data from thousands of RFID devices and sensors at the edge before selectively pushing valuable insights to the cloud. By way of concise description, the platform is an edge computing architecture for cost optimization and scalable proceesing of massive streaming data from IoT devices

## Why This Project Matters

##### In an era where IoT devices are projected to generate 79.4 zettabytes of data annually, enterprises face the challenge of extracting value without incurring massive cloud costs. This project provides the architectural blueprint for:

  * Intelligent edge computing that processes data where it is generated

  * Cost-effective scalability that grows with business needs

  * Real-time analytics that drive immediate business decisions

  * Future-proof architecture that adapts to evolving IoT landscapes

This isn't just a technical demonstration, it is a production-proven foundation for enterprise IoT transformation that delivers immediate ROI through reduced cloud costs and enhanced operational intelligence.

---


## Critical Enterprise Value Propositions

* Massive-Scale Real-time Analytics
  
* 10,000+ concurrent device handling with demonstrated processing of 5+ million records

* Sub-second latency from edge to analytics-ready data

* Enterprise-grade reliability with zero data loss architecture

* Scalable Kafka-based streaming that grows with your IoT deployment

### <ins>Key Advantages</ins>: Process terabytes of raw sensor data locally, then send only kilobytes of business intelligence to the cloud, thereby reducing:

* Cloud infrastructure costs by 60-80%

* Data egress charges through intelligent filtering

* Network bandwidth requirements

* Cloud processing expenses

### <ins>Industrial IoT (IIoT) Ready</ins>

Real-time asset tracking across manufacturing floors

Predictive maintenance through continuous equipment monitoring

Supply chain visibility from raw materials to customer delivery

Quality control with environmental condition tracking

Regulatory compliance through comprehensive audit trails


### <ins>Enterprise Streaming Data Pipeline Architecture</ins>

* Modern Streaming Foundation


```ruby

     RFID/IIoT Devices → Kafka Stream Processing → PostgreSQL Data Warehouse → Cloud Analytics
       ↓                    ↓                       ↓                      ↓
   Edge Data          Real-time              Structured Data        Business Intelligence
   Collection         Processing               Storage                 & Dashboards
  
```

### <ins>Strategic Design Benefits</ins>

1. Separation of Concerns (as shown in the figure below)

    * Kafka: Handles raw data ingestion and real-time processing

    * PostgreSQL: Provides structured storage and complex query capabilities

    * Cloud Export: Enables selective data synchronization
      
  
  ![Image](https://github.com/user-attachments/assets/670a6e6d-ec2c-4826-ba61-757ac3ff986a)


2. Fault Tolerance & Resilience

    * Message durability through Kafka persistence

    * Data integrity with transactional database operations

    * Disconnected operation capability during network outages


3. Technology Agnostic

    * Interchangeable components (Kafka → RabbitMQ, PostgreSQL → TimescaleDB)

    * Cloud vendor independence - deploy on-premises or any cloud provider

    * Protocol flexibility - supports MQTT, HTTP, and custom protocols
  
  ---

## Enterprise Use Cases

### <ins>Retail & Inventory Management</ins>  🏪 

* Real-time inventory tracking with RFID tags

* Automated price lookups and updates

* Theft prevention through real-time monitoring

* Smart shelf management with temperature monitoring

* Customer behavior analysis through product interaction tracking

### <ins>Manufacturing & Industrial IoT (IIoT)</ins> 🏪

* Asset tracking across production lines

* Equipment temperature monitoring for predictive maintenance

* Supply chain visibility from raw materials to finished goods

* Quality control with environmental condition monitoring

* Work-in-progress tracking through manufacturing stages

### <ins>Smart Buildings & Facilities</ins> 🏪

* Access control with RFID badges

* Equipment monitoring and maintenance scheduling

* Environmental monitoring (temperature, humidity)

* Asset location tracking across facilities

* Energy management through equipment usage tracking

### <ins>Logistics & Supply Chain</ins>  🏪

* Real-time shipment tracking

* Cold chain monitoring for perishable goods

* Warehouse inventory management

* Cross-docking operations optimization

* Delivery route optimization

### <ins>Healthcare & Pharmaceuticals</ins>  🏪

* Medical equipment tracking

* Temperature-sensitive medication monitoring

* Patient and staff movement tracking

* Asset utilization optimization

* Regulatory compliance monitoring

### <ins>Key Features</ins> 🏪

* Massive IoT Streaming Capabilities

* 10,000+ concurrent device simulation

* Real-time data processing at enterprise scale

* High-throughput message handling (5M+ records demonstrated)

* Low-latency data ingestion (<1 second end-to-end)

### <ins>Edge Computing Advantages</ins> 🏪

* Local data processing reduces cloud dependency

* Bandwidth optimization - only processed data sent to cloud

* Offline operation capability during network outages

* Real-time decision making at the edge

### <ins>Cost Optimization</ins> 🏪

* Reduced cloud infrastructure costs - process data locally

* Pay-per-use cloud services - only export valuable insights

* Minimal data egress charges - send summarized data, not raw streams

* Scalable architecture - pay only for what you need

---

## Project Structure

```ruby

rfid-iot-pipeline/
├── docker-compose.yml
├── kafka-producer/
│   ├── producer.py
│   ├── requirements.txt
│   └── Dockerfile
├── kafka-consumer/
│   ├── consumer.py
│   ├── requirements.txt
│   └── Dockerfile
├── cloud-push/
│   ├── push.py
│   ├── requirements.txt
│   └── Dockerfile
├── init-db/
│   └── init.sql
└── cloud_data/
    ├── temperature_*.csv
    └── price_*.csv
  
```

### Quick Start (prerequisites)

* Docker Desktop 20.10+

* Docker Compose 2.0+

* 4GB+ RAM available

* Git

### Installation & Setup

* Clone the Repository

```ruby
git clone https://github.com/manuelbomi/RFID-IIoT-Pipeline------Enterprise-Grade-IoT-Streaming-Platform-with-Kafka-PostgreSQL-Docker.git
cd rfid-iot-pipeline
```

* Start the Complete Stack
  
```ruby
docker-compose up -d
```

* Wait for Services to Initialize (30-60 seconds)

```ruby
# Check all services are running
docker-compose ps
```

* Create Kafka Topics (if not auto-created)
  
```ruby
# Create temperature reads topic
docker-compose exec kafka kafka-topics --create \
  --topic temperature_reads \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Create price lookups topic
docker-compose exec kafka kafka-topics --create \
  --topic price_lookups \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

* Verify Topics Creation
  
```ruby
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```


#### Below are examples of some outputs using VSCode:

```ruby
docker-compose up -d

```

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/79bafaae-78a4-4bb9-b4b6-09d56a77a2cb" />



<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/843b327b-8f85-476b-a16f-890c1c468315" />


**Both producer and consumer working**

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/d4023c4d-b63d-4dfc-a916-a59a8bf91246" />


**Data insertion test and data quality test**

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/d11392d4-4527-446e-8a9d-cbd648c6a8fa" />

**Streaming data from both temperature (IoT) and prices (RFID) tables**

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/9ae2cb7b-37bd-455c-8576-8a8ea2692f8a" />


**Database growing as more data stream into the tables**

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/735148a7-7a4d-4451-a707-56804ffbd44e" />


**How to manually start up Kafka producer and consumer topics in case it doesn't auto start**

*docker-compose up -d producer consumer*

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/aff6106a-adbc-44f9-bf11-c498859d325c" />

---






## Technical Configuration

### <ins>Kafka Topic Management</ins>

* Create Partitioned Topics for Scaling

```ruby

# For high-volume applications, use multiple partitions
docker-compose exec kafka kafka-topics --create \
  --topic temperature_reads \
  --bootstrap-server localhost:9092 \
  --partitions 10 \
  --replication-factor 1

docker-compose exec kafka kafka-topics --create \
  --topic price_lookups \
  --bootstrap-server localhost:9092 \
  --partitions 5 \
  --replication-factor 1

```

* Monitor Kafka Topic Performance

```ruby

# Check topic details
docker-compose exec kafka kafka-topics --describe --bootstrap-server localhost:9092

# Monitor message rates
docker-compose exec kafka kafka-run-class kafka.tools.GetOffsetShell \
  --bootstrap-server localhost:9092 \
  --topic temperature_reads --time -1

```

* Consumer Group Management


```ruby

# List consumer groups
docker-compose exec kafka kafka-consumer-groups --list --bootstrap-server localhost:9092

# Check consumer lag
docker-compose exec kafka kafka-consumer-groups --describe \
  --group rfid_temperature_ingestor \
  --bootstrap-server localhost:9092


```

* Data Formats

<ins>Temperature Read Events</ins>

```ruby

{
  "event": "temperature_read",
  "epc": "3014B2C3D4E5F6",
  "temperature": 1.5,
  "unit": "C",
  "timestamp": "2025-10-05T18:00:00Z"
}


```

<ins>Price Lookup Events</ins>

```ruby
{
  "event": "price_lookup",
  "epc": "3014B2C3D4E5F6",
  "item_details": {
    "name": "Leather Jacket",
    "sku": "LJ-4577",
    "price": 199.99,
    "currency": "USD"
  },
  "timestamp": "2025-10-05T18:00:00Z"
}

```

---

### Database  (PostgreSQL) Interaction

* Using pgAdmin Web Interface
  
Access pgAdmin: <ins>http://localhost:8080</ins>

```ruby
Login Credentials:

Email: admin@rfid.com

Password: admin

Add PostgreSQL Server:

Name: RFID PostgreSQL

Host: postgres

Port: 5432

Database: rfiddb

Username: rfiduser

Password: rfidpass

Useful SQL Queries

```

#### Alternately, after using <ins>admin@rfid.com</ins> and password <ins>admin</ins> to login via pgadmi, you can copy pgadmin server login parameters from the docker-compose file

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/317e6072-6613-4224-ac47-307bdeb8303d" />


<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/41dda18d-3294-4406-a250-3737e2c93d2d" />


<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/b232f3a9-bf45-4f6d-aca4-1a47b4e86de1" />


#### To query the tables via PostgreSQL pgAdmin, select the database, click on tools and select Query Tools

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/764981ea-419d-4d77-b14f-3f7861f6fd6e" />


#### Count the records in temperature_reads table

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/6766fe8c-7892-4904-bc2d-f6262e908ebb" />


#### Real time analytics

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/3f7c3cbe-6ba6-4ebb-9eb4-c86950b52834" />


#### Price lookup analytics

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/4d285f6d-e7c8-49fa-9d3f-2f7184814219" />

####  Device monitoring

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/45125e0a-c6f3-4627-9a95-94be812375bb" />

#### Business intelligence SQL queries

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/89159f87-15c6-4b1c-86e4-cdab79cdca03" />

#### Prodcut popularity analysis

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/25ea1771-2de1-476f-9a06-fd68d4f1d912" />

#### Temperature trend analysis

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/5d26f995-3e2c-4b59-a736-81c28bf60254" />


