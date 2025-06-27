import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import agents using absolute imports that work when package is in Python path
try:
    # Try relative imports first (when imported as part of package)
    from ..agents.data_loader import DataLoaderAgent
    from ..agents.markdown_responder import MarkdownResponderAgent
    from ..agents.sql_executor import SQLExecutorAgent
    from ..agents.sql_generator import SQLGeneratorAgent
except ImportError:
    # Fall back to absolute imports (when src is in Python path)
    from edgar_query.agents.data_loader import DataLoaderAgent
    from edgar_query.agents.markdown_responder import MarkdownResponderAgent
    from edgar_query.agents.sql_executor import SQLExecutorAgent
    from edgar_query.agents.sql_generator import SQLGeneratorAgent

app = FastAPI(title="EDGAR Filings Query API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize data agent and connection at startup
data_agent = DataLoaderAgent()
conn = data_agent.init_db()

# Initialize other agents
sql_agent = SQLGeneratorAgent()
markdown_agent = MarkdownResponderAgent()

# Check if data needs to be loaded
filings_count = pd.read_sql_query("SELECT COUNT(*) as count FROM filings", conn).iloc[
    0
]["count"]
if filings_count == 0:
    print("Loading SEC filings data...")
    data_agent.load_master_index()
    print("Data loading complete.")


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    markdown_response: str | None = None
    sql_query: str | None = None
    error: str | None = None


@app.post("/query", response_model=QueryResponse)
async def query_filings(request: QueryRequest):
    """
    Process a natural language query about SEC filings and return a formatted response.
    """
    try:
        # Generate SQL query from natural language
        sql_query, prompt = sql_agent.generate_sql_query(request.query)

        if not sql_query:
            return QueryResponse(error="Could not generate SQL query from the input")

        # Execute the SQL query
        sql_executor = SQLExecutorAgent(conn)
        df, error = sql_executor.execute_sql_query(sql_query)

        if error:
            return QueryResponse(error=error, sql_query=sql_query)

        # Generate markdown response
        markdown_response, _ = markdown_agent.generate_markdown_response(
            request.query, sql_query, df
        )

        return QueryResponse(markdown_response=markdown_response, sql_query=sql_query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        filings_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM filings", conn
        ).iloc[0]["count"]
        form_types = pd.read_sql_query(
            "SELECT form_type, COUNT(*) as count FROM filings GROUP BY form_type ORDER BY count DESC LIMIT 10",
            conn,
        )

        return {
            "total_filings": int(filings_count),
            "top_form_types": form_types.to_dict("records"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def main():
    """Main entry point for the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
