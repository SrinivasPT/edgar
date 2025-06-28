"""Core functionality for EDGAR query tool."""

from typing import Any, Dict

from ..agents import (
    DataLoaderAgent,
    MarkdownResponderAgent,
    SQLExecutorAgent,
    SQLGeneratorAgent,
)


class EdgarQueryEngine:
    """Main query engine for EDGAR filings."""

    def __init__(self):
        self.data_loader = DataLoaderAgent()
        self.sql_generator = SQLGeneratorAgent()
        self.markdown_responder = MarkdownResponderAgent()
        self.sql_executor = None

    def initialize(self):
        """Initialize the database connection."""
        conn = self.data_loader.init_db()
        self.sql_executor = SQLExecutorAgent(conn)
        return conn

    def query(self, user_query: str) -> Dict[str, Any]:
        """Execute a natural language query and return formatted results."""
        if not self.sql_executor:
            raise RuntimeError("Engine not initialized. Call initialize() first.")

        # Generate SQL from natural language
        sql_query, prompt = self.sql_generator.generate_sql_query(user_query)
        if not sql_query:
            return {
                "success": False,
                "error": "Could not generate SQL query",
                "sql_prompt": prompt,
            }

        # Execute SQL query
        df, error = self.sql_executor.execute_sql_query(sql_query)
        if error:
            return {"success": False, "error": error, "sql_prompt": prompt}

        # Generate markdown response
        markdown_response, response_prompt = (
            self.markdown_responder.generate_markdown_response(
                user_query, sql_query, df
            )
        )

        return {
            "success": True,
            "sql_query": sql_query,
            "data": df,
            "markdown_response": markdown_response,
            "sql_prompt": prompt,
            "response_prompt": response_prompt,
        }
