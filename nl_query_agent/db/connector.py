import psycopg2
from ..config import DB_CONFIG, SCHEMA

class PostgresConnector:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def run_query(self, sql: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SET search_path TO {SCHEMA};")
                cur.execute(sql)
                return {
                    "columns": [desc[0] for desc in cur.description],
                    "rows": cur.fetchall()
                }
        except Exception as e:
            self.conn.rollback()   # 🔑 reset the transaction so next queries work
            raise


    def close(self):
        self.conn.close()
