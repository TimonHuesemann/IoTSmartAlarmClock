import sqlite3



class DatabaseManager:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable row access by name
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None





    def create_table(self, table_name, columns):
        """Create a table with the specified name and columns."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        columns_with_types = ', '.join(columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")
        self.connection.commit()

    def insert_data(self, table_name, data, replace=False):
        """Insert data into the specified table. If replace=True, use INSERT OR REPLACE."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        placeholders = ', '.join('?' for _ in data)
        if replace:
            cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})", data)
        else:
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.connection.commit()

    def drop_table(self, table_name):
        """Drop the specified table from the database."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    def fetch_all(self, table_name):
        """Fetch all rows from the specified table."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows
    

    def fetch_one(self, table_name, condition):
        """Fetch a single row from the specified table based on a condition."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        row = cursor.fetchone()
        return row