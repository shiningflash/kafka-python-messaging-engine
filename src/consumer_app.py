import os
from dotenv import load_dotenv

from src.kafka.schema_client_registry import SchemaClient
from src.kafka.avro_consumer import AvroKafkaConsumer
from src.logger import setup_logger

logger = setup_logger(__name__)
load_dotenv()


def load_schema(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def main():
    bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:19092")
    topic = os.getenv("KAFKA_TOPIC", "user-topic")
    group_id = os.getenv("KAFKA_GROUP_ID", "default-consumer-group")
    schema_url = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:18081")
    schema_type = os.getenv("SCHEMA_TYPE", "AVRO")
    schema_path = os.getenv("AVRO_SCHEMA_PATH", "src/schemas/user.avsc")

    avro_schema = load_schema(schema_path)

    schema_client = SchemaClient(
        schema_url=schema_url,
        subject_name=topic,
        schema_str=avro_schema,
        schema_type=schema_type
    )

    consumer = AvroKafkaConsumer(
        bootstrap_server=bootstrap_server,
        topic=topic,
        group_id=group_id,
        schema_registry_client=schema_client.client,
        schema_str=schema_client.fetch_schema_str()
    )

    logger.info("Kafka Consumer starting...")
    consumer.start()


if __name__ == "__main__":
    main()
