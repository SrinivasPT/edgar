# API Documentation

## Overview

The EDGAR Filings Query API provides programmatic access to SEC EDGAR filing data using natural language queries. This API converts natural language questions into SQL queries, executes them against the SEC filings database, and returns formatted responses.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Query Endpoint

`POST /query`

Process a natural language query about SEC filings.

#### Request Format

```json
{
  "query": "string"
}
```

#### Parameters

| Name  | Type   | Description                                             |
|-------|--------|---------------------------------------------------------|
| query | string | A natural language question about SEC EDGAR filings      |

#### Response Format

```json
{
  "markdown_response": "string",
  "sql_query": "string",
  "error": "string"
}
```

#### Response Fields

| Name              | Type   | Description                                                |
|-------------------|--------|------------------------------------------------------------|
| markdown_response | string | Formatted response to the query as markdown                |
| sql_query         | string | The SQL query that was generated and executed (optional)   |
| error             | string | Error message if query processing failed (optional)        |

#### Example Request

```bash
curl -X 'POST' \
  'http://localhost:8000/query' \
  -H 'Content-Type: application/json' \
  -d '{"query": "How many 10-K filings were made?"}'
```

#### Example Response

```json
{
  "markdown_response": "There were 938 10-K filings made in Q1 2025.",
  "sql_query": "SELECT COUNT(*) FROM filings WHERE form_type = '10-K'"
}
```

### Health Check

`GET /health`

Simple health check endpoint to verify the API is running.

#### Response

```json
{
  "status": "healthy"
}
```

## Error Handling

The API may return the following error responses:

| Status Code | Description                                              |
|-------------|----------------------------------------------------------|
| 400         | Bad Request - Query parameter is missing or empty        |
| 500         | Internal Server Error - Error in processing the query    |

## Interactive Documentation

When the API is running, you can access the automatic Swagger documentation at:

```
http://localhost:8000/docs
```

This provides an interactive interface to test API endpoints directly.
