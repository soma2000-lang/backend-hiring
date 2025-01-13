from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.conf import settings
from vanderval.db.config import DatabaseManager
import psycopg
from psycopg.errors import OperationalError


class DatabaseManagerTests(TestCase):
    def setUp(self):
        DatabaseManager._DatabaseManager__instance = None
        self.database_manager = DatabaseManager()

    def tearDown(self):
        if self.database_manager._database_connection:
            self.database_manager.close()
        self.database_manager = None

    def test_singleton_ensures_single_instance(self):
        database_manager1 = DatabaseManager()
        database_manager2 = DatabaseManager()
        self.assertIs(database_manager1, database_manager2)

    @patch("todo_project.db.config.psycopg.connect")
    def test_initializes_db_connection_on_first_call(self, mock_connect):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_connect.return_value = mock_connection
        
        db_connection = self.database_manager._get_database_connection()

        mock_connect.assert_called_once_with(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        self.assertIs(db_connection, mock_connection)

    @patch("todo_project.db.config.psycopg.connect")
    def test_reuses_existing_connection_on_subsequent_calls(self, mock_connect):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_connect.return_value = mock_connection

        connection1 = self.database_manager._get_database_connection()
        connection2 = self.database_manager._get_database_connection()

        mock_connect.assert_called_once()
        self.assertIs(connection1, connection2)

    @patch("todo_project.db.config.DatabaseManager._get_database_connection")
    def test_initializes_cursor_on_first_call(self, mock_get_connection):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        cursor = self.database_manager.get_cursor()

        mock_get_connection.assert_called_once()
        mock_connection.cursor.assert_called_once()
        self.assertIs(cursor, mock_cursor)

    @patch("todo_project.db.config.DatabaseManager._get_database_connection")
    def test_reuses_existing_cursor_on_subsequent_calls(self, mock_get_connection):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        cursor1 = self.database_manager.get_cursor()
        cursor2 = self.database_manager.get_cursor()

        mock_connection.cursor.assert_called_once()
        self.assertIs(cursor1, cursor2)

    @patch("todo_project.db.config.DatabaseManager.get_cursor")
    def test_execute_query_with_params(self, mock_get_cursor):
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        mock_get_cursor.return_value = mock_cursor

        query = "SELECT * FROM test WHERE id = %s"
        params = (1,)
        self.database_manager.execute_query(query, params)

        mock_get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query, params)

    @patch("todo_project.db.config.DatabaseManager.get_cursor")
    def test_fetch_all_returns_all_results(self, mock_get_cursor):
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        expected_results = [(1, 'test'), (2, 'test2')]
        mock_cursor.fetchall.return_value = expected_results
        mock_get_cursor.return_value = mock_cursor

        results = self.database_manager.fetch_all("SELECT * FROM test")

        self.assertEqual(results, expected_results)
        mock_cursor.fetchall.assert_called_once()

    @patch("todo_project.db.config.DatabaseManager._get_database_connection")
    def test_check_db_health_returns_true_on_successful_connection(self, mock_get_connection):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        result = self.database_manager.check_database_health()

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with("SELECT 1")

    @patch("todo_project.db.config.DatabaseManager._get_database_connection")
    def test_check_db_health_returns_false_on_connection_failure(self, mock_get_connection):
        mock_get_connection.side_effect = OperationalError("Mocked connection failure")

        result = self.database_manager.check_database_health()

        self.assertFalse(result)

    def test_close_cleans_up_resources(self):
        mock_connection = MagicMock(spec=psycopg.Connection)
        mock_cursor = MagicMock(spec=psycopg.Cursor)
        self.database_manager._database_connection = mock_connection
        self.database_manager._cursor = mock_cursor

        self.database_manager.close()

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertIsNone(self.database_manager._database_connection)
        self.assertIsNone(self.database_manager._cursor)