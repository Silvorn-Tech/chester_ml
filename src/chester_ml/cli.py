import argparse
import os
from loguru import logger
from dotenv import load_dotenv

from chester_ml.utils.logger_controller import log_mode, dynamic_log
from chester_ml.core import execute_providers
from chester_ml.utils.env_controller import check_env
from chester_ml.providers.database_providers.sql_controller import SQLController
from chester_ml.providers.database_providers.mongo_controller import MongoController


def setup_logger():
    """Configura los niveles de log del entorno Chester."""
    load_dotenv()
    logger_level = os.getenv("LOGGER_LEVELS", "ALL")
    logger.remove()
    log_mode(logger_level)


def check_status():
    """Verifica la carga del .env y el estado real de las conexiones SQL y Mongo (estilo dinámico tipo Poetry)."""
    logger.info("🔍 Checking Chester environment and connections...")
    check_env()
    load_dotenv()

    sql_config = {
        "host": os.getenv("SQL_HOST"),
        "user": os.getenv("SQL_USER"),
        "password": os.getenv("SQL_PASSWORD"),
        "database": os.getenv("SQL_DATABASE")
    }
    mongo_config = {
        "uri": os.getenv("MONGO_URI"),
        "database": os.getenv("MONGO_DATABASE"),
        "collection": os.getenv("MONGO_COLLECTION")
    }

    logger.info("🧩 Environment Variables Check:")
    logger.info("───────────────────────────────")

    logger.info("🗄️  Checking SQL Configuration...")
    sql_status = False
    dynamic_log("   ", "Connecting to SQL...")
    try:
        sql = SQLController(**sql_config)
        if sql.test_connection():
            logger.info("✅ SQL connection: OK (database reachable)")
            sql_status = True
        else:
            logger.error("❌ SQL connection: FAILED (unreachable or misconfigured)")
    except Exception as e:
        logger.error(f"❌ SQL connection error: {e}")

    logger.info("───────────────────────────────")

    # ===== Mongo Check =====
    logger.info("🍃 Checking MongoDB Configuration...")
    mongo_status = False
    dynamic_log("   ", "Connecting to MongoDB...")
    try:
        mongo = MongoController(**mongo_config)
        if mongo.test_connection():
            logger.info("✅ MongoDB connection: OK (cluster reachable)")
            mongo_status = True
        else:
            logger.error("❌ MongoDB connection: FAILED (no response)")
    except Exception as e:
        logger.error(f"❌ MongoDB connection error: {e}")

    logger.info("───────────────────────────────")

    # ===== Result Summary =====
    if sql_status and mongo_status:
        logger.info("🎯 All systems operational — environment and databases loaded successfully.")
    elif sql_status or mongo_status:
        logger.warning("⚠️ Partial connectivity — at least one provider is unavailable.")
    else:
        logger.error("🚨 No providers reachable — check environment configuration.")

    logger.info("✅ Status check complete.")


def main():
    """Punto de entrada principal del CLI de Chester ML."""
    setup_logger()

    parser = argparse.ArgumentParser(description="Chester ML CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Comando: run
    run_parser = subparsers.add_parser("run", help="Ejecuta uno o varios proveedores de datos")
    run_parser.add_argument(
        "providers",
        nargs="+",
        choices=["sql", "mongo", "files", "all"],
        help="Proveedores a ejecutar (sql, mongo, files o all)"
    )
    run_parser.add_argument(
        "--output",
        help="Ruta opcional para guardar los resultados en formato JSON"
    )

    # Comando: status
    subparsers.add_parser("status", help="Verifica las conexiones y el entorno Chester")

    args = parser.parse_args()

    if args.command == "run":
        execute_providers(args.providers, args.output)
    elif args.command == "status":
        check_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
