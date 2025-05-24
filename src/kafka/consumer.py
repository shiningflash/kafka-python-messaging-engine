from confluent_kafka import Consumer, KafkaException
from src.logger import setup_logger

logger = setup_logger(__name__)


class KafkaConsumer:
    """
    KafkaConsumer handles message consumption from a Kafka topic.
    """
    def __init__(self, bootstrap_server: str, topic: str, group_id: str):
        self.topic = topic
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def start(self) -> None:
        """
        Subscribe and begin consuming messages.
        """
        self.consumer.subscribe([self.topic])
        logger.info(f"Subscribed to topic: {self.topic}")

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue
                logger.info(f"Consumed message: {msg.value().decode('utf-8')}")
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user.")
        except KafkaException as e:
            logger.exception("Kafka error occurred.")
        finally:
            self.consumer.close()
            logger.info("Consumer shutdown cleanly.")
