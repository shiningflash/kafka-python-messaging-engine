import os
from dotenv import load_dotenv
from src.kafka.avro_producer import AvroKafkaProducer
from src.kafka.admin import KafkaAdmin
from src.kafka.schema_client_registry import SchemaClient
from src.logger import setup_logger
from src.schemas.user import User

load_dotenv()
logger = setup_logger(__name__)


def load_schema(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def main():
    bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:19092")
    topic = os.getenv("KAFKA_TOPIC", "user-topic")
    schema_url = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:18081")
    schema_file_path = os.getenv("AVRO_SCHEMA_PATH", "src/schemas/user.avsc")
    schema_type = os.getenv("SCHEMA_TYPE", "AVRO")

    # Create topic if not exists
    admin = KafkaAdmin(bootstrap_server)
    admin.create_topic(topic)

    # Register the schema
    avro_schema = load_schema(schema_file_path)
    schema_client = SchemaClient(
        schema_url=schema_url,
        subject_name=topic,
        schema_str=avro_schema,
        schema_type=schema_type
    )
    schema_client.register_schema()

    producer = AvroKafkaProducer(
        bootstrap_server=bootstrap_server,
        topic=topic,
        schema_registry_client=schema_client.client,
        schema_str=schema_client.fetch_schema_str(),
        message_delay=float(os.getenv("PRODUCER_MESSAGE_DELAY", 0.0))
    )

    logger.info("Kafka Avro Producer is ready. Press Ctrl+C to exit.")

    try:
        while True:
            try:
                first_name = input("Enter your first name: ").strip()
                last_name = input("Enter your last name: ").strip()
                age_input = input("Enter your age: ").strip()
                if not age_input.isdigit():
                    logger.warning("Age must be a valid integer.")
                    continue

                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    age=int(age_input)
                )
                producer.send_message(user.to_dict())
            except Exception as e:
                logger.error(f"Error in sending message: {e}")
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
        producer.commit()


if __name__ == "__main__":
    main()
