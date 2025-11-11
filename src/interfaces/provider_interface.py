from abc import ABC, abstractmethod

class ProviderInterface(ABC):
    """
    Base interface for all data providers.
    Ensures consistent methods for connection, reading, and writing data
    across structured, semi-structured, and unstructured sources.
    """
    @abstractmethod
    def test_connection(self):
        """
        Test-only connection or access verification.

        Each provider should implement this method to validate
        that its underlying data source is reachable and configured correctly.
        - SQL → intenta abrir y cerrar una conexión temporal.
        - Mongo → ejecuta un ping.
        - Files → verifica existencia y permisos de lectura/escritura.
        """
        pass

    @abstractmethod
    def connect(self):
        """Establishes a connection with the data source."""
        pass

    @abstractmethod
    def read(self, query=None):
        """
        Reads data from the source.
        - For SQL: expects a SQL query string.
        - For Mongo: expects a filter dictionary.
        - For files: can ignore or use path/query parameters.
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        Writes data to the source.
        - For SQL: performs INSERT or UPDATE.
        - For Mongo: performs insert_one/insert_many.
        - For files: writes to a file.
        """
        pass

    @abstractmethod
    def close(self):
        """Closes the connection or resource if applicable."""
        pass
