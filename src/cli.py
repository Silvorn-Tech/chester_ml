import os
import argparse
import traceback

from loguru import logger
from dotenv import load_dotenv

from src.utils.logger_controller import setup_logger
from src.utils.env_controller import check_env
from src.core import execute





def main():
    try:
        load_dotenv()

        parser = argparse.ArgumentParser(description="Chester ML CLI")
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser("status", help="Verifica el archivo .env")
        subparsers.add_parser("run", help="Ejecuta la aplicación principal")

        args = parser.parse_args()

        setup_logger(os.getenv("LOGGER_LEVELS", "ALL"))

        if args.command == "status":
            check_env()
        elif args.command == "run":
            execute()
        else:
            parser.print_help()

    except Exception as e:
        print("❌ Error al ejecutar Chester:")
        traceback.print_exc()
        logger.error(str(e))


if __name__ == "__main__":
    main()
