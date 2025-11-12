import os
from dotenv import load_dotenv
from loguru import logger
from chester_ml.providers.database_providers.sql_controller import SQLController
from chester_ml.providers.database_providers.mongo_controller import MongoController


class RemoteEngine:
    """Handles remote data sources: SQL, MongoDB, APIs."""

    def __init__(self):
        logger.debug("🔧 Initializing RemoteEngine...")
        load_dotenv()
        logger.debug("🌍 Environment variables loaded.")

    def execute(self, provider_type, statement):
        logger.info(f"🚀 Executing remote provider: {provider_type}")
        logger.debug(f"📜 Statement received: {statement}")

        try:
            if provider_type == "SQL":
                return self._execute_sql(statement)
            elif provider_type == "MONGO":
                return self._execute_mongo(statement)
            else:
                raise ValueError(f"Unsupported remote provider: {provider_type}")
        except Exception as e:
            logger.error(f"❌ RemoteEngine execution error for {provider_type}: {e}")
            return None


    def _execute_sql(self, statement):
        logger.debug("🧩 Preparing SQL controller configuration...")
        sql = SQLController(
            host=os.getenv("SQL_HOST"),
            user=os.getenv("SQL_USER"),
            password=os.getenv("SQL_PASSWORD"),
            database=os.getenv("SQL_DATABASE")
        )
        logger.debug(f"📦 SQL configuration: {sql.config}")

        try:
            logger.info("🔌 Connecting to SQL database...")
            sql.connect()
            logger.info("✅ SQL connection established.")

            query = statement.get("query")
            if not query:
                logger.warning("⚠️ No query found in SQL statement.")
                return None

            logger.debug(f"▶️ Executing SQL query: {query}")
            result = sql.read(query)

            if result:
                logger.info(f"📊 Query returned {len(result)} rows.")
            else:
                logger.warning("⚠️ Query executed successfully but returned no results.")

            return result

        except Exception as e:
            logger.error(f"❌ SQL execution failed: {e}")
            return None
        finally:
            logger.debug("🔒 Closing SQL connection...")
            sql.close()
            logger.debug("🧩 SQL connection closed.")


    def _execute_mongo(self, statement):
        logger.debug("🧩 Preparing MongoDB controller configuration...")
        mongo = MongoController(
            uri=os.getenv("MONGO_URI"),
            database=os.getenv("MONGO_DATABASE"),
            collection=statement.get("collection", os.getenv("MONGO_COLLECTION"))
        )
        logger.debug(f"📦 Mongo configuration: uri={mongo.uri}, db={mongo.database_name}, col={mongo.collection_name}")

        try:
            logger.info("🔌 Connecting to MongoDB...")
            mongo.connect()
            logger.info("✅ MongoDB connection established.")

            filter_query = statement.get("filter", {})
            logger.debug(f"▶️ Executing MongoDB query: {filter_query}")

            result = mongo.read(filter_query)

            if result:
                logger.info(f"📊 Query returned {len(result)} documents.")
            else:
                logger.warning("⚠️ MongoDB query executed successfully but returned no results.")

            return result

        except Exception as e:
            logger.error(f"❌ MongoDB execution failed: {e}")
            return None
        finally:
            logger.debug("🔒 Closing MongoDB connection...")
            mongo.close()
            logger.debug("🧩 MongoDB connection closed.")
