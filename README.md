# kafka-python-messaging-engine

A modular, schema-aware messaging engine built in **Python** with **Kafka** and **Avro**, using **Redpanda** as the Kafka backend.

This project includes:
- ✅ Avro serialization with Schema Registry
- ✅ Producer and consumer interfaces
- ✅ Batch support, delivery reports, tombstone messages
- ✅ Fully configurable via `.env` (see `.env.example`)
- ✅ Managed using [Poetry](https://python-poetry.org)

---

## Tech Stack

- **Python 3.11+**
- **Poetry** for dependency management
- **Redpanda** (Kafka-compatible streaming platform)
- **Confluent Kafka Python Client**
- **Avro + Schema Registry**

---

## Getting Started (with Docker + Redpanda)

Redpanda is used to run a Kafka-compatible stack locally with minimal effort.

### 1. Clone the repo

```bash
git clone https://github.com/shiningflash/kafka-python-messaging-engine.git
cd kafka-python-messaging-engine
````

### 2. Start Redpanda and Schema Registry (via Docker)

```bash
docker compose up -d
```

> This starts:
>
> * Redpanda Kafka Broker at `localhost:19092`
> * Redpanda Schema Registry at `http://localhost:18081`
> * Redpanda Console UI at `http://localhost:8080`

### 3. Check Services

* **Kafka Broker**: `localhost:19092`
* **Schema Registry**: `http://localhost:18081`
* **Redpanda Console**: [http://localhost:8080](http://localhost:8080)

---

## Environment Configuration

Copy and modify your environment variables:

```bash
cp .env.example .env
```

Edit `.env` to suit your local or dev settings.

---

## Schema Location

User Avro schema lives in:

```
src/schemas/user.avsc
```

Update the schema and `.env` accordingly if you modify fields.

---

## Python Setup (via Poetry)

### Install Dependencies

```bash
poetry install
```

### Activate the Virtual Env

```bash
poetry env activate
```

---

## 🚀 Run Producer App

```bash
python -m src.producer_app
```

This will:

* Connect to Redpanda
* Prompt you to input user data
* Send serialized Avro messages to Kafka

---

## 🎧 Run Consumer App

```bash
python -m src.consumer_app
```

This will:

* Connect to the same topic
* Consume and deserialize Avro messages
* Support batch reads (configurable in `.env`)

---

## Learn More

To get familiar with Kafka, its role in streaming pipelines, and design concepts, check the beginner-friendly guide:

👉 [intro\_to\_kafka.md](intro_to_kafka.md)

---

## Contributing

Pull requests welcome! Please:

* Keep code clean and modular
* Write meaningful commit messages
* Follow PEP8 and type hinting conventions

---

## 📝 License

MIT License — feel free to use, fork, and contribute.
