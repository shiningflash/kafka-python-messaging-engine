from src.kafka.schema_client_registry import SchemaClient
from src.kafka.avro_consumer import AvroKafkaConsumer
from src.logger import setup_logger

logger = setup_logger(__name__)


def main():
    bootstrap_server = "localhost:19092"
    topic = "user-topic"
    group_id = "default-consumer-group"
    
    schema_url = "http://localhost:18081"
    schema_type = "AVRO"
    
    avro_schema_file_path = "src/schemas/user.avsc"
    
    with open(avro_schema_file_path) as avro_file:
        avro_schema = avro_file.read()
        
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
        schema_client_registry=schema_client.schema_registry_client,
        schema_str=schema_client.get_schema_str()
    )
    logger.info("Kafka Consumer starting...")
    consumer.start()


if __name__ == "__main__":
    main()
