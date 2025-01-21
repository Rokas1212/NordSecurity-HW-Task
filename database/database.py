import sqlite3
import json
from datetime import datetime

"""
SQLite connection handler class

"""
class SqliteHandler():

    _instance = None

    def __new__(cls, database):
        """
            Singleton pattern to ensure only one instance of the class is created
            database: Path to the SQLite database
            returns: SqliteHandler object
        """

        # If an instance of the class does not exist, create one, otherwise return the existing instance
        if cls._instance is None:
            cls._instance = super(SqliteHandler, cls).__new__(cls)
            cls._instance._connection = sqlite3.connect(database)
            cls._instance.cursor = cls._instance._connection.cursor()
        return cls._instance

    def fetch_all_table_rows(self, table_name, column_mapping):
        """
            Fetch all rows from the table
            table_name: Name of the table
            column_mapping: Dictionary of column mappings
            returns: List of rows
        """
        # Convert column names to a comma-separated string
        columns_str = ', '.join(column_mapping.values())

        # Get the date column from the column mapping
        date_column = column_mapping["contract_expiration"]

        # Query to fetch all rows from the table where the date is greater than or equal to today
        query = f"SELECT {columns_str} FROM {table_name} WHERE DATE({date_column}) >= DATE('now')"

        # Execute the query
        self.cursor.execute(query)

        # Fetch all rows
        rows = self.cursor.fetchall()

        return rows

# For testing purposes
if __name__ == "__main__":
    # Read table schemas file
    with open('table_schemas.json', 'r') as file:
        table_schemas = json.load(file)

    sqlite_handler = SqliteHandler("contracts.sqlite")

    # Iterate through each table and display its data
    for table, columns in table_schemas.items():
        print(f"\nOrganization: {table}")
        rows = sqlite_handler.fetch_all_table_rows(table, columns)
        for row in rows:
            print(row)


