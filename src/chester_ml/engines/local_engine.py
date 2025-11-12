from loguru import logger
from chester_ml.providers.file_providers import FileProvider

class LocalEngine:
    """Handles local data sources: JSON, CSV, TXT."""
    def execute(self, provider_type, statement):
        if provider_type == "FILES":
            return self._execute_file(statement)
        else:
            raise ValueError(f"Unsupported local provider: {provider_type}")

    def _execute_file(self, statement):
        file = FileProvider(statement["path"])
        file.connect()
        data = file.read()
        return data
