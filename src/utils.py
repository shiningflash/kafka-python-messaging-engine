from src.logger import setup_logger

logger = setup_logger(__name__)


def delivery_report(err, msg) -> None:
    """
    Kafka delivery report callback.

    Args:
        err: The error (if any) returned by the broker.
        msg: The Kafka message that was sent.
    """
    if err:
        logger.error(f"Failed to deliver message {msg.key()}: {err}")
    else:
        logger.info(
            f"Delivered message to {msg.topic()} [partition {msg.partition()}] "
            f"at offset {msg.offset()} | key={msg.key()}"
        )
