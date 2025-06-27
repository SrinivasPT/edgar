import pandas as pd


class SQLExecutorService:
    def __init__(self, conn):
        self.conn = conn

    def execute_sql_query(self, sql_query):
        try:
            forbidden = [
                "DROP",
                "DELETE",
                "INSERT",
                "UPDATE",
                "CREATE",
                "ALTER",
                "TRUNCATE",
            ]
            if any(keyword in sql_query.upper() for keyword in forbidden):
                return None, "Query contains forbidden operations"
            df = pd.read_sql_query(sql_query, self.conn)
            return df, None
        except Exception as e:
            return None, f"Error executing query: {e}"
