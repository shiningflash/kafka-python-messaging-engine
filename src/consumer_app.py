from src.kafka.consumer import KafkaConsumer
from src.logger import setup_logger

logger = setup_logger(__name__)


def main():
    bootstrap_server = "localhost:19092"
    topic = "test-topic"
    group_id = "default-consumer-group"

    consumer = KafkaConsumer(bootstrap_server, topic, group_id)
    logger.info("Kafka Consumer starting...")
    consumer.start()


if __name__ == "__main__":
    main()
