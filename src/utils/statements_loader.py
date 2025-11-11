import json
import os
from loguru import logger

class StatementsLoader:
    def __init__(self, universe_dir="universes"):
        self.universe_dir = universe_dir
        self.remote_statements = {}
        self.local_statements = {}

    def load_statements(self):
        """Carga los archivos de configuración de negocio."""
        try:
            for file in os.listdir(self.universe_dir):
                path = os.path.join(self.universe_dir, file)
                if not file.endswith(".json"):
                    continue

                with open(path, "r", encoding="utf-8") as f:
                    content = json.load(f)

                if "remote" in file.lower():
                    self.remote_statements.update(content)
                elif "loca" in file.lower():
                    self.local_statements.update(content)

            logger.info("✅ Business configurations (remote/local) loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load business configurations: {e}")

    def get_statement(self, context, provider_type, key):
        """
        Obtiene una configuración según el contexto.
        context = 'remote' | 'local'
        provider_type = 'SQL' | 'MONGO' | 'FILES'
        key = nombre de la consulta o archivo
        """
        if context == "remote":
            provider = self.remote_statements.get(provider_type.upper(), {})
        elif context == "local":
            provider = self.local_statements.get(provider_type.upper(), {})
        else:
            logger.error(f"❌ Invalid context '{context}'. Use 'remote' or 'local'.")
            return None

        statement = provider.get(key)
        if not statement:
            logger.warning(f"⚠️ Statement '{key}' not found for provider '{provider_type}' in {context}.")
        return statement
