from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

from src.logger import setup_logger

logger = setup_logger(__name__)


class AvroKafkaConsumer:
    """
    AvroKafkaConsumer handles message consumption from a Kafka topic.
    """
    def __init__(self, bootstrap_server: str, topic: str, group_id: str, schema_client_registry, schema_str):
        self.topic = topic
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.value_deserializer = AvroDeserializer(
            schema_registry_client=schema_client_registry,
            schema_str=schema_str
        )

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
                byte_message = msg.value()
                logger.info(f"Byte message: {byte_message}. Type: {type(byte_message)}")
                deserialized_message = self.value_deserializer(
                    data=byte_message,
                    ctx=SerializationContext(
                        topic=self.topic,
                        field=MessageField.VALUE
                    )
                )
                logger.info(f"Deserialized message: {deserialized_message}. Type: {type(deserialized_message)}")
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user.")
        except KafkaException as e:
            logger.exception("Kafka error occurred.")
        finally:
            self.consumer.close()
            logger.info("Consumer shutdown cleanly.")
