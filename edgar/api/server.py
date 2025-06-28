from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from edgar.services.data_loader import DataLoaderService
from edgar.services.markdown_responder import MarkdownResponderService
from edgar.services.sql_executor import SQLExecutorService
from edgar.services.sql_generator import SQLGeneratorService

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
data_agent = DataLoaderService()
conn = data_agent.init_db()

# Initialize other agents
sql_agent = SQLGeneratorService()
markdown_agent = MarkdownResponderService()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    markdown_response: Optional[str] = None
    sql_query: Optional[str] = None
    error: Optional[str] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


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
        sql_executor = SQLExecutorService(conn)
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


def main():
    """Main entry point for the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
