from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..core.engine import EdgarQueryEngine

app = FastAPI(title="EDGAR Filings Query API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
        engine = EdgarQueryEngine()
        engine.initialize()
        response = engine.query(request.query)
        return QueryResponse(
            markdown_response=response["markdown_response"],
            sql_query=response["sql_query"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def main():
    """Main entry point for the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
