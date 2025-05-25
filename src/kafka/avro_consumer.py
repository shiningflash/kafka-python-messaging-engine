from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

from src.logger import setup_logger

logger = setup_logger(__name__)


class AvroKafkaConsumer:
    """
    AvroKafkaConsumer handles Avro-encoded batch consumption from a Kafka topic.
    """

    def __init__(
        self,
        bootstrap_server: str,
        topic: str,
        group_id: str,
        schema_registry_client,
        schema_str: str,
        batch_size: int = 10,
        poll_timeout: float = 1.0
    ):
        self.topic = topic
        self.batch_size = batch_size
        self.poll_timeout = poll_timeout
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.value_deserializer = AvroDeserializer(schema_registry_client, schema_str)

    def start(self) -> None:
        self.consumer.subscribe([self.topic])
        logger.info(f"Subscribed to topic: {self.topic}")

        try:
            while True:
                messages = self.consumer.consume(num_messages=self.batch_size, timeout=self.poll_timeout)
                for msg in messages:
                    if msg is None:
                        continue
                    if msg.error():
                        logger.error(f"Kafka error: {msg.error()}")
                        continue

                    raw_value = msg.value()
                    if raw_value is None:
                        logger.info(f"Received tombstone for key={msg.key()}")
                        continue

                    deserialized = self.value_deserializer(
                        data=raw_value,
                        ctx=SerializationContext(self.topic, MessageField.VALUE)
                    )
                    logger.info(f"Consumed message: {deserialized}")
        except KeyboardInterrupt:
            logger.info("Consumer interrupted.")
        except KafkaException:
            logger.exception("Kafka exception during consumption.")
        finally:
            self.consumer.close()
            logger.info("Consumer shutdown cleanly.")
