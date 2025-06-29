import psycopg2
import psycopg2.extras



class DatabaseManager:
    def __init__(self, dbname, user, password, host='db', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.connection.autocommit = True
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
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});')
        cursor.close()



    def insert_data(self, table_name, data, primary_key_names="", replace=False):
        """
        Insert data into the specified table.
        If replace=True, use UPSERT (ON CONFLICT DO UPDATE).
        primary_key_names should be a string of comma-separated primary key column names.
        """
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        if replace:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
            columns = [row[0] for row in cursor.fetchall()]

            update_stmt = ', '.join([f"{col}=EXCLUDED.{col}" for col in columns if col not in primary_key_names.split(',')])
            cursor.execute(
                f"INSERT INTO {table_name} VALUES ({placeholders}) "
                f"ON CONFLICT ({primary_key_names}) DO UPDATE SET {update_stmt};",
                data
            )
        else:
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", data)
        cursor.close()




    def drop_table(self, table_name):
        """Drop the specified table from the database."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.close()

    def fetch_all(self, table_name):
        """Fetch all rows from the specified table."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_one(self, table_name, condition):
        """Fetch a single row from the specified table based on a condition."""
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row