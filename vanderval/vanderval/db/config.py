import logging
import psycopg
from django.conf import settings
from psycopg.errors import OperationalError

logger = logging.getLogger(__name__)

class DatabaseManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance._database_connection = None
            cls.__instance._cursor = None
        return cls.__instance

    def _get_database_connection(self):
        if self._database_connection is None:
            self._database_connection = psycopg.connect(
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT
            )
        return self._database_connection

    def get_cursor(self):
        if self._cursor is None:
            connection = self._get_database_connection()
            self._cursor = connection.cursor()
        return self._cursor

    def execute_query(self, query, params=None):
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    def check_database_health(self):
        try:
            connection = self._get_database_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            logger.info("Database connection established successfully")
            return True
        except OperationalError as e:
            logger.error(f"Failed to establish database connection: {e}")
            return False

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._database_connection:
            self._database_connection.close()
            self._database_connection = None
            self._cursor = None