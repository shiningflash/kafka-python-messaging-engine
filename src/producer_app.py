from src.kafka.producer import KafkaProducer
from src.kafka.admin import KafkaAdmin
from src.logger import setup_logger

logger = setup_logger(__name__)


def main():
    bootstrap_server = "localhost:19092"
    topic = "test-topic"

    admin = KafkaAdmin(bootstrap_server)
    admin.create_topic(topic)

    producer = KafkaProducer(bootstrap_server, topic)
    logger.info("Kafka Producer is ready. Press Ctrl+C to stop sending.")

    try:
        while True:
            message = input("Enter your message: ")
            if message.strip():
                producer.send_message(message)
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
        producer.commit()


if __name__ == "__main__":
    main()
