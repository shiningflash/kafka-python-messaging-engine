# Introduction to Kafka for Python Developers

Apache Kafka is a high-performance, distributed streaming platform designed for real-time data pipelines and event-driven architectures.

This guide explains:
- What Kafka is
- How it works
- How to use Kafka with Python
- Key concepts like Avro, schema registry, tombstones, cleanup policies, and compression
- Configuration best practices

---

## Why Kafka?

Kafka enables:
- Real-time **data pipelines**
- Event-driven **microservices**
- High-throughput **stream processing**
- Decoupling between **data producers and consumers**
- Long-term **durable message storage**

---

## Kafka Components

| Component         | Description                                                             |
|-------------------|-------------------------------------------------------------------------|
| **Producer**      | Sends messages to a topic                                               |
| **Consumer**      | Reads messages from a topic                                             |
| **Broker**        | Kafka server, stores and manages messages                               |
| **Topic**         | Named stream of records                                                 |
| **Partition**     | Parallel units of a topic                                               |
| **Offset**        | Unique ID of a message within a partition                               |
| **Consumer Group**| Set of consumers sharing load of a topic                                |
| **Schema Registry** | Manages versioned schemas (e.g., Avro)                                |

---

## Kafka Architecture

```text
                         +-------------------+
                         |   Schema Registry |
                         |  (Avro Schemas)   |
                         +--------▲----------+
                                  |
                                  |
                (validate + fetch/write schema ID)
                                  |
+--------------------+     +------|-----------+
|  Python Producer   |     |  Avro Serializer |
|--------------------|     +------------------+
|  - input() / json  |             |
|  - validate schema |             v
|  - call AvroSerializer()     Serialized bytes
|  - set key          +----------------------------+
|                     |    Compression (Snappy)    |
|                     +----------------------------+
|                         |                        |
|                     Kafka Record            Kafka Key (String)
|                         |                        |
+------------+------------+                        |
             |                                     |
             v                                     v
     +-------------------------------+     +---------------------+
     |    Kafka Broker (Redpanda)    |     |     Topic Store     |
     | - Receives compressed record  |     | - Partitioned log   |
     | - Stores record by key        |     | - Optional compaction|
     +---------------+---------------+     +---------------------+
                     |
               Consumes from topic
                     |
                     v
     +-------------------------------+
     |   Python Avro Consumer        |
     |-------------------------------|
     | - Reads Kafka record          |
     | - Calls AvroDeserializer      |
     | - Fetch schema ID from SR     |
     | - Deserialize to Python dict  |
     +-------------------------------+
```

---

## Kafka Producer: Key Concepts

### Basic Configuration

```python
from confluent_kafka import Producer

producer = Producer({
    'bootstrap.servers': 'localhost:19092',
    'compression.type': 'snappy',
    'batch.size': 16384,
    'linger.ms': 5,
})
```

| Key                | Description                                                 |
| ------------------ | ----------------------------------------------------------- |
| `compression.type` | gzip, snappy, lz4 — reduces bandwidth & improves throughput |
| `batch.size`       | Max bytes per batch before sending                          |
| `linger.ms`        | Time to wait before sending a batch                         |

### Flush and Delivery Callback

```python
def delivery_report(err, msg):
    if err:
        print("❌ Delivery failed:", err)
    else:
        print("✅ Message delivered:", msg.key(), msg.offset())

producer.produce("my-topic", key="id1", value="data", on_delivery=delivery_report)
producer.flush()
```

---

## Avro, Schema Registry, and Serialization

### Why Schema?

* Validates data structure
* Prevents schema drift
* Enables schema evolution

### Avro Record Example

```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "first_name", "type": "string" },
    { "name": "last_name", "type": "string" },
    { "name": "age", "type": "int" }
  ]
}
```

### Producer with Avro

```python
from confluent_kafka.schema_registry.avro import AvroSerializer

serializer = AvroSerializer(schema_registry_client, schema_str)
serialized = serializer(message, SerializationContext(topic, MessageField.VALUE))
```

---

## Kafka Consumer with Avro

```python
from confluent_kafka.schema_registry.avro import AvroDeserializer

deserializer = AvroDeserializer(schema_registry_client, schema_str)
msg = consumer.poll()
data = deserializer(msg.value(), SerializationContext(topic, MessageField.VALUE))
```

---

## Tombstone Messages (Deleting a Record)

Kafka uses **tombstone messages** to delete a record from a **compacted** topic.

### How It Works

* A tombstone is a message with a key and a **null value**
* Kafka **ignores earlier messages** with the same key
* Kafka marks the key for deletion in log-compacted topics

### Example:

```python
producer.produce(topic="user-topic", key="user-123", value=None)
```

### ⚠️ Important:

To make this work:

```properties
cleanup.policy=compact
```

### When to Use:

* Logical deletes
* Keyed updates (most recent key wins)
* Efficient storage for stateful services

---

## ⚠️ `auto.offset.reset`

Controls what a consumer does when no initial offset is found:

| Value      | Behavior                                |
| ---------- | --------------------------------------- |
| `earliest` | Start from beginning of partition       |
| `latest`   | Only new messages after consumer starts |
| `none`     | Throw error if no offset is found       |

---

## Usage Scenarios

### 1. User Activity Tracking

* Producer: web app sends click events
* Consumer: logs events to DB for analytics

### 2. Order Pipeline

* Producer: ecommerce app creates orders
* Consumer: warehouse app processes them

### 3. Log Compaction for User Profiles

* Topic stores user profile by ID
* Updates overwrite earlier messages
* Tombstone deletes the user

---

## Best Practices

| Area               | Practice                                             |
| ------------------ | ---------------------------------------------------- |
| Topic design       | Use meaningful names, e.g., `user-events`            |
| Schema evolution   | Use optional fields instead of deleting fields       |
| Compression        | Use `snappy` or `lz4` for fast encoding              |
| Delivery guarantee | Handle `delivery_report` properly                    |
| Tombstones         | Use for deletes on compacted topics only             |
| Environment config | Keep Kafka configs in `.env`, version `.env.example` |
| Consumer groups    | Use a unique `group.id` per logical use case         |
| Graceful shutdown  | Always `flush()` producer and `close()` consumer     |
| Batch processing   | Use `consume(num_messages=N)` to reduce overhead     |

---

## Tools Used

* [Redpanda](https://redpanda.com/)
* [Confluent Kafka Python](https://github.com/confluentinc/confluent-kafka-python)
* [Apache Avro](https://avro.apache.org/)
* [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)

---

## Summary

Kafka is a powerful backbone for building scalable, real-time data platforms. Combined with Python, Avro, and a schema registry, you get:

* Type-safe messages
* Scalable decoupled systems
* Real-time analytics and stateful pipelines

Explore the code, configure your `.env`, and run the producer/consumer to get started!

Happy streaming! 🚀
