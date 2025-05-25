from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.error import SchemaRegistryError
from src.logger import setup_logger

logger = setup_logger(__name__)


class SchemaClient:
    """
    Handles interaction with the Confluent Schema Registry.
    """

    def __init__(self, schema_url: str, subject_name: str, schema_str: str, schema_type: str = "AVRO") -> None:
        self.subject_name = subject_name
        self.schema_str = schema_str
        self.schema_type = schema_type.upper()
        self.client = SchemaRegistryClient({"url": schema_url})

    def get_latest_schema_id(self) -> int | None:
        """
        Retrieves the schema ID for the latest version of a subject.
        Returns None if not found.
        """
        try:
            version_info = self.client.get_latest_version(self.subject_name)
            return version_info.schema_id
        except SchemaRegistryError as e:
            logger.warning(f"No existing schema found for subject '{self.subject_name}': {e}")
            return None

    def fetch_schema_str(self) -> str | None:
        """
        Fetches the schema string using the latest schema ID.
        """
        schema_id = self.get_latest_schema_id()
        if schema_id is None:
            logger.warning("No schema ID available to fetch schema string.")
            return None
        try:
            schema = self.client.get_schema(schema_id)
            return schema.schema_str
        except SchemaRegistryError as e:
            logger.error(f"Failed to fetch schema for ID {schema_id}: {e}")
            return None

    def register_schema(self) -> bool:
        """
        Registers a new schema if one is not already registered.
        Returns True if a new schema is registered, False otherwise.
        """
        if self.get_latest_schema_id() is not None:
            logger.info("Schema already registered.")
            return False

        try:
            schema = Schema(self.schema_str, self.schema_type)
            self.client.register_schema(self.subject_name, schema)
            logger.info(f"Schema registered successfully for subject '{self.subject_name}'.")
            return True
        except SchemaRegistryError as e:
            logger.error(f"Failed to register schema: {e}")
            return False
