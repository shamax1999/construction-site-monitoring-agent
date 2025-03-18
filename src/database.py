import psycopg2

from src.config import DatabaseConfig
from src.models import SensorReading

class Database:
    def __init__(self, config: 'DatabaseConfig'):
        self.conn_params = config.dict()
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Database connection established")
        except psycopg2.Error as e:
            print(f"Failed to connect to database: {e}")
            raise

    def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                temperature FLOAT,
                vibration FLOAT,
                noise FLOAT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS actions (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                message TEXT NOT NULL
            )
            """
        ]
        try:
            with self.conn.cursor() as cur:
                for query in queries:
                    cur.execute(query)
                self.conn.commit()
            print("Database tables verified/created")
        except psycopg2.Error as e:
            print(f"Failed to create tables: {e}")
            self.conn.rollback()
            raise

    def log_reading(self, reading: SensorReading):
        query = """
            INSERT INTO sensor_readings (temperature, vibration, noise)
            VALUES (%s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (reading.temperature, reading.vibration, reading.noise))
            self.conn.commit()

    def log_action(self, message: str):
        query = "INSERT INTO actions (message) VALUES (%s)"
        with self.conn.cursor() as cur:
            cur.execute(query, (message,))
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")