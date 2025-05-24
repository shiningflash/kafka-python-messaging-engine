from confluent_kafka import Producer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

from src.kafka.producer import KafkaProducer
from src.logger import setup_logger

logger = setup_logger(__name__)


class AvroKafkaProducer(KafkaProducer):
    """
    AvroKafkaProducer handles message production to a Kafka topic.
    """
    def __init__(self, bootstrap_server: str, topic: str, schema_registry_client, schema_str):
        super().__init__(bootstrap_server=bootstrap_server, topic=topic)
        self.schema_registry_client = schema_registry_client
        self.schema_str = schema_str
        self.value_serializer = AvroSerializer(
            schema_registry_client=schema_registry_client,
            schema_str=schema_str
        )

    def send_message(self, message: str) -> None:
        try:
            avro_byte_message = self.value_serializer(
                obj=message,
                ctx=SerializationContext(
                    topic=self.topic,
                    field=MessageField.VALUE
                )
            )
            self.producer.produce(self.topic, avro_byte_message)
            logger.info(f"Message sent: {avro_byte_message}")
        except BufferError as e:
            logger.error(f"Local producer queue is full: {e}")
        except Exception as e:
            logger.exception("Exception while sending message")

    def commit(self) -> None:
        self.producer.flush()
