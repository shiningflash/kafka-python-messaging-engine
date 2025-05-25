from src.logger import setup_logger

logger = setup_logger(__name__)


def delivery_report(err, msg):
    if err:
        logger.error(f"Failed to deliver message {msg.key()}: str({err})")
        return
    logger.info(f"Successfully delivered message {msg.key()} to topic {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}")
