import mysql.connector
from chester_ml.interfaces.provider_interface import ProviderInterface
from loguru import logger

class SQLController(ProviderInterface):
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.connection = None
        self.cursor = None

    def test_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            conn.close()
            return True
        except Exception:
            return False


    def connect(self):
        try:
            logger.debug(f"Connecting to SQL with config: {self.config}")
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("✅ SQL connection established.")
        except Exception as e:
            logger.error(f"❌ SQL connection failed 11: {e}")


    def read(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def write(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logger.info("✅ Query executed successfully.")
        except Exception as e:
            logger.error(f"Error executing write query: {e}")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logger.info("🔒 SQL connection closed.")
