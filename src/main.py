import threading
from src.kafka.producer import KafkaProducer
from src.kafka.consumer import KafkaConsumer
from src.kafka.admin import KafkaAdmin
from src.logger import setup_logger

logger = setup_logger(__name__)


def run_producer(bootstrap_server: str, topic: str) -> None:
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


def run_consumer(bootstrap_server: str, topic: str, group_id: str) -> None:
    consumer = KafkaConsumer(bootstrap_server, topic, group_id)
    consumer.start()


def main():
    bootstrap_server = "localhost:19092"
    topic = "test-topic"
    group_id = "my-consumer-group"

    admin = KafkaAdmin(bootstrap_server)
    admin.create_topic(topic)

    # Start consumer in a separate thread
    consumer_thread = threading.Thread(
        target=run_consumer, args=(bootstrap_server, topic, group_id), daemon=True
    )
    consumer_thread.start()

    # Run producer in main thread
    run_producer(bootstrap_server, topic)


if __name__ == "__main__":
    main()
