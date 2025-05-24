from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.error import SchemaRegistryError

from src.logger import setup_logger

logger = setup_logger(__name__)


class SchemaClient:
    def __init__(self, schema_url, subject_name, schema_str, schema_type):
        self.schema_url = schema_url
        self.subject_name = subject_name
        self.schema_str = schema_str
        self.schema_type = schema_type
        self.schema_registry_client = SchemaRegistryClient({"url": self.schema_url})
    
    def get_schema_version(self):
        try:
            schema_version = self.schema_registry_client.get_latest_version(self.subject_name)
            return schema_version.schema_id
        except SchemaRegistryError:
            return False
    
    def get_schema_str(self):
        try:
            schema_id = self.get_schema_version()
            schema = self.schema_registry_client.get_schema(schema_id=schema_id)
            return schema.schema_str
        except SchemaRegistryError as e:
            logger.error(f"Error in get schema string: {e}")
    
    def register_schema(self):
        if not self.get_schema_version():
            try:
                schema = Schema(self.schema_str, self.schema_type)
                self.schema_registry_client.register_schema(self.subject_name, schema)
                logger.info("Schema registered successfully!")
            except SchemaRegistryError as e:
                 logger.error(f"Error in register schema: {e}")
        else:
            logger.info("Schema already registered!")
