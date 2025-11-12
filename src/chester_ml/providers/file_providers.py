import json
import os
from chester_ml.interfaces.provider_interface import ProviderInterface
from loguru import logger

class FileProvider(ProviderInterface):
    def __init__(self, filepath):
        self.filepath = filepath

    def test_connection(self):
        try:
            return os.path.exists(self.path)
        except Exception:
            return False


    def connect(self):
        if os.path.exists(self.filepath):
            logger.info(f"📂 File ready: {self.filepath}")
        else:
            logger.warning(f"⚠️ File not found: {self.filepath}")

    def read(self, _=None):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            logger.info(f"✅ File read successfully: {self.filepath}")
            return data
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None

    def write(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            logger.info(f"✅ File written successfully: {self.filepath}")
        except Exception as e:
            logger.error(f"Error writing file: {e}")

    def close(self):
        logger.debug("🧾 File provider does not require close operation.")
