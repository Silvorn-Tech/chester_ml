from pymongo import MongoClient
from chester_ml.interfaces.provider_interface import ProviderInterface
from loguru import logger
from chester_ml.utils.logger_controller import dynamic_log


class MongoController(ProviderInterface):
    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database_name = database
        self.collection_name = collection
        self.client = None
        self.collection = None

    def test_connection(self):
        """Quick test for Chester status command."""
        try:
            client = MongoClient(self.uri, serverSelectionTimeoutMS=1500)
            client.admin.command("ping")
            client.close()
            return True
        except Exception:
            return False

    def connect(self):
        """Establish a MongoDB connection with visual feedback."""
        logger.debug(f"Preparing to connect to MongoDB at {self.uri} "
                     f"(DB: {self.database_name}, Collection: {self.collection_name})")

        dynamic_log("   ", f"Connecting to MongoDB at {self.uri} ...")

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            self.collection = self.client[self.database_name][self.collection_name]
            logger.success("✅ MongoDB connection established.")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")

    def read(self, query=None):
        """Read documents with dynamic progress feedback."""
        dynamic_log("   ", f"Reading data from collection '{self.collection_name}' ...")
        try:
            data = list(self.collection.find(query or {}))
            logger.success(f"✅ Retrieved {len(data)} records from MongoDB collection '{self.collection_name}'.")
            return data
        except Exception as e:
            logger.error(f"❌ Error reading from MongoDB: {e}")
            return None

    def write(self, data):
        """Write one or many documents to the collection."""
        try:
            if isinstance(data, list):
                self.collection.insert_many(data)
            else:
                self.collection.insert_one(data)
            logger.success("✅ Data written successfully to MongoDB.")
        except Exception as e:
            logger.error(f"❌ Error writing to MongoDB: {e}")

    def close(self):
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()
            logger.info("🔒 MongoDB connection closed.")
