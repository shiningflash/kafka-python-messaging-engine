from src.kafka.avro_producer import AvroKafkaProducer
from src.kafka.admin import KafkaAdmin
from src.kafka.schema_client_registry import SchemaClient
from src.logger import setup_logger
from src.schemas.user import User

logger = setup_logger(__name__)


def main():
    bootstrap_server = "localhost:19092"
    topic = "user-topic"
    
    schema_url = "http://localhost:18081"
    schema_type = "AVRO"

    # Create topic
    admin = KafkaAdmin(bootstrap_server)
    admin.create_topic(topic)
    
    avro_schema_file_path = "src/schemas/user.avsc"

    # Register the schema
    with open(avro_schema_file_path) as avro_file:
        avro_schema = avro_file.read()
        
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
        schema_registry_client=schema_client.schema_registry_client,
        schema_str=schema_client.get_schema_str()
    )
    logger.info("Kafka Producer is ready. Press Ctrl+C to stop sending.")

    try:
        while True:
            try:
                first_name = input("Enter your first name: ").strip()
                last_name = input("Enter your last name: ").strip()
                age = int(input("Enter your age: ").strip())
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    age=age
                )
                producer.send_message(user.to_dict())
            except Exception as e:
                logger.error(f"Error in sending message: str({e})")
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
        producer.commit()


if __name__ == "__main__":
    main()
