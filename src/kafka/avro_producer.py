import time
from uuid import uuid4
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer

from src.kafka.producer import KafkaProducer
from src.logger import setup_logger
from src.utils import delivery_report

logger = setup_logger(__name__)


class AvroKafkaProducer(KafkaProducer):
    """
    AvroKafkaProducer handles Avro-encoded message production to a Kafka topic.
    """

    def __init__(
        self,
        bootstrap_server: str,
        topic: str,
        schema_registry_client,
        schema_str: str,
        compression_type: str = "snappy",
        message_delay: float = 0.0
    ):
        super().__init__(bootstrap_server, topic, config={"compression.type": compression_type})
        self.value_serializer = AvroSerializer(schema_registry_client, schema_str)
        self.key_serializer = StringSerializer("utf_8")
        self.message_delay = message_delay  # seconds between messages

    def send_message(self, message: dict, key: str | None = None, is_tombstone: bool = False) -> None:
        """
        Sends an Avro-encoded message to Kafka. Use `is_tombstone=True` to send a tombstone.
        """
        try:
            correlation_id = key or str(uuid4())

            serialized_value = None if is_tombstone else self.value_serializer(
                obj=message,
                ctx=SerializationContext(self.topic, MessageField.VALUE)
            )

            self.producer.produce(
                topic=self.topic,
                key=self.key_serializer(correlation_id),
                value=serialized_value,
                headers={"correlation_id": correlation_id},
                on_delivery=delivery_report
            )
            logger.info(f"Produced {'tombstone' if is_tombstone else 'message'}: {correlation_id}")
            if self.message_delay:
                time.sleep(self.message_delay)

        except BufferError as e:
            logger.error(f"Producer buffer is full: {e}")
        except Exception:
            logger.exception("Failed to send Avro message")

    def commit(self) -> None:
        self.producer.flush()
