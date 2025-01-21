import unittest
from sqlite3 import OperationalError
from datetime import datetime, timedelta
from db_handlers.sqlite_handler import SqliteHandler

class TestSqliteHandler(unittest.TestCase):

    def setUp(self):
        """Set up an in-memory SQLite database for testing."""
        # Reset the singleton instance
        SqliteHandler._instance = None

        self.db = SqliteHandler(":memory:")
        self.db.cursor.execute("CREATE TABLE contracts (name TEXT, contract_expiration TEXT)"
                               )
        today = datetime.now().strftime('%Y-%m-%d')
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        past_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        self.db.cursor.executemany(
            "INSERT INTO contracts (name, contract_expiration) VALUES (?, ?)",
            [
                ('Contract Today', today), 
                ('Contract Future', future_date),
                ('Contract Expired', past_date),
            ]
        )
        self.db._connection.commit()

    def tearDown(self):
        """Tear down the database connection."""
        self.db.close_connection()


    def test_fetch_all_table_rows(self):
        """Test fetching rows that have expiration dates today or in the future."""
        column_mapping = {
            "name": "name",
            "contract_expiration": "contract_expiration"
        }

        rows = self.db.fetch_all_table_rows("contracts", column_mapping)

        # Only two rows should be returned: one with today's date and one in the future
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], 'Contract Today')
        self.assertEqual(rows[1][0], 'Contract Future')

    def test_singleton_pattern(self):
        """Test that the Singleton pattern works correctly."""
        db1 = SqliteHandler(":memory:")
        db2 = SqliteHandler(":memory:")
        self.assertIs(db1, db2)

    def test_close_connection(self):
        db = SqliteHandler(":memory:")
        db.close_connection()
        self.assertIsNone(db._instance)


    def test_invalid_table_name(self):
        """
        Test handling of an invalid table name.
        Should also complain in the console that the table name is invalid.
        """
        column_mapping = {
            "name": "name",
            "contract_expiration": "contract_expiration"
        }
        # Attempt to fetch rows from a non-existent table
        rows = self.db.fetch_all_table_rows("nonexistent_table", column_mapping)
        self.assertEqual(len(rows), 0) 
    
    def test_invalid_column_name(self):
        """
        Test handling of an invalid column name.
        Should also complain in the console that
        there was an error fetching from the specific table.
        """
        # Attempt to fetch rows using an invalid column name
        rows = self.db.fetch_all_table_rows("contracts", {"invalid_column": "name"})
        self.assertEqual(len(rows), 0)