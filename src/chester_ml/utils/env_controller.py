from loguru import logger
from dotenv import find_dotenv, load_dotenv


def check_env():
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path)
        logger.debug(f"✅ Se esta cargando el archivo en la ruta: {env_path}")
    else:
        logger.error("⚠️ No se encontró archivo .env en el proyecto.")

