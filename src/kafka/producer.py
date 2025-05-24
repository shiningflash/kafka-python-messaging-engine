from confluent_kafka import Producer
from src.logger import setup_logger

logger = setup_logger(__name__)


class KafkaProducer:
    """
    KafkaProducer handles message production to a Kafka topic.
    """
    def __init__(self, bootstrap_server: str, topic: str, config: dict = None):
        self.topic = topic
        producer_config = {"bootstrap.servers": bootstrap_server}
        if config:
            producer_config.update(config)
        self.producer = Producer(producer_config)

    def send_message(self, message: str) -> None:
        try:
            self.producer.produce(self.topic, message)
        except BufferError as e:
            logger.error(f"Local producer queue is full: {e}")
        except Exception as e:
            logger.exception("Exception while sending message")

    def commit(self) -> None:
        self.producer.flush()
