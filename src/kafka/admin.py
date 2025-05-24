from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from src.logger import setup_logger

logger = setup_logger(__name__)


class KafkaAdmin:
    """
    KafkaAdmin is responsible for managing Kafka topics.
    """
    def __init__(self, bootstrap_server: str):
        self.bootstrap_server = bootstrap_server
        self.admin = AdminClient({"bootstrap.servers": self.bootstrap_server})

    def topic_exists(self, topic: str) -> bool:
        metadata = self.admin.list_topics(timeout=5)
        return topic in metadata.topics

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> bool:
        if self.topic_exists(topic):
            logger.info(f"Topic '{topic}' already exists.")
            return False

        new_topic = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)

        try:
            futures = self.admin.create_topics([new_topic])
            futures[topic].result()  # Block until complete or error
            logger.info(f"Topic '{topic}' created successfully.")
            return True
        except KafkaException as e:
            logger.error(f"Failed to create topic '{topic}': {e}")
        except Exception as e:
            logger.exception("Unexpected error during topic creation")

        return False
