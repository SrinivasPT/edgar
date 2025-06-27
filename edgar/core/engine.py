"""Core functionality for EDGAR query tool."""

from ..services import (
    DataLoaderService,
    MarkdownResponderService,
    SQLExecutorService,
    SQLGeneratorService,
)


class EdgarQueryEngine:
    """Main query engine for EDGAR filings."""

    def __init__(self):
        self.data_loader = DataLoaderService()
        self.sql_generator = SQLGeneratorService()
        self.markdown_responder = MarkdownResponderService()
        self.sql_executor = None

    def initialize(self):
        """Initialize the database connection."""
        conn = self.data_loader.init_db()
        self.sql_executor = SQLExecutorService(conn)
        return conn

    def load_data(self):
        """Load EDGAR filing data into the database."""
        return self.data_loader.load_master_index()

    def query(self, user_query):
        """Execute a natural language query and return formatted results."""
        if not self.sql_executor:
            raise RuntimeError("Engine not initialized. Call initialize() first.")

        # Generate SQL from natural language
        sql_query, prompt = self.sql_generator.generate_sql_query(user_query)
        if not sql_query:
            return None, "Could not generate SQL query", prompt

        # Execute SQL query
        df, error = self.sql_executor.execute_sql_query(sql_query)
        if error:
            return None, error, prompt

        # Generate markdown response
        markdown_response, response_prompt = (
            self.markdown_responder.generate_markdown_response(
                user_query, sql_query, df
            )
        )

        return (
            {
                "sql_query": sql_query,
                "data": df,
                "markdown_response": markdown_response,
                "sql_prompt": prompt,
                "response_prompt": response_prompt,
            },
            None,
            None,
        )
