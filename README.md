# EDGAR Filings Query Tool with AI

An intelligent SEC EDGAR filings query tool that leverages Large Language Models (LLMs) to generate SQL queries from natural language and provide intelligent responses.

> **New Feature**: The tool now includes a FastAPI endpoint that allows programmatic access to the same query functionality. See [API documentation](./API_DOCS.md) for details.

## Features

- 🤖 **AI-Powered Query Generation**: Uses OpenAI's GPT to convert natural language queries into SQL
- 📊 **Intelligent Response Formatting**: LLM analyzes query results and provides clear, informative responses
- 🔍 **Natural Language Interface**: Ask questions in plain English about SEC filings
- 📈 **Real-time Data**: Loads Q1 2025 SEC EDGAR master index
- 🛡️ **SQL Injection Protection**: Safe query execution with forbidden keyword filtering
- 📱 **Modern UI**: Clean Streamlit interface with example queries and statistics

## Installation

1. Clone or download the project

2. Install `uv` (if not already installed):
   ```bash
   # Windows PowerShell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:
   ```bash
   # Install all dependencies (uv automatically creates virtual environment)
   uv sync
   
   # Or install with development dependencies
   uv sync --dev
   ```

4. Set up your OpenAI API key:
   ```bash
   # Windows Command Prompt
   set OPENAI_API_KEY=your_api_key_here
   
   # Windows PowerShell
   $env:OPENAI_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export OPENAI_API_KEY="your_api_key_here"
   ```

5. Run the application:
   ```bash
   # Run both the FastAPI server and web app (Windows)
   scripts\start_services.bat
   
   # Or run individually:
   # Run just the API server
   edgar-api
   
   # Run just the web server
   edgar-web
   
   # Development commands:
   python dev.py test           # Run tests
   python dev.py lint-fix       # Fix code issues
   python dev.py format         # Format code
   python dev.py qa            # Full quality check
   ```

## Usage

### Example Queries

The tool can understand and respond to natural language queries such as:

- **Counting queries**: "How many 10-K filings were made in Q1 2025?"
- **Company-specific queries**: "Show me all filings from Apple"
- **Form type analysis**: "What are the most common form types?"
- **Company information**: "What is the SIC code for Microsoft?"
- **Filing patterns**: "Which companies filed the most documents?"

### Features

1. **Example Queries**: Click on pre-built example queries to get started
2. **SQL Transparency**: Toggle "Show generated SQL queries" in the sidebar to see the AI-generated SQL
3. **Database Statistics**: View real-time statistics about the loaded data
4. **Fallback Mode**: If OpenAI API is not available, falls back to rule-based processing

## How It Works

1. **Query Processing**: User enters a natural language query
2. **SQL Generation**: OpenAI GPT analyzes the query and database schema to generate appropriate SQL
3. **Safe Execution**: SQL is validated and executed safely against the SQLite database
4. **Intelligent Response**: GPT analyzes the results and provides a clear, informative response

## Database Schema

The tool works with two main tables:

### filings
- `cik`: Company Central Index Key
- `company_name`: Official company name
- `form_type`: SEC form type (10-K, 10-Q, 8-K, etc.)
- `date_filed`: Filing date
- `filename`: Path to the filing document

### companies
- `cik`: Company Central Index Key (Primary Key)
- `name`: Company name
- `sic`: Standard Industrial Classification code
- `business_address`: Company business address

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI features

### Streamlit Configuration
- The tool uses Streamlit's session state to manage UI interactions
- SQL query visibility can be toggled via the sidebar

## Error Handling

- **No API Key**: Falls back to rule-based query processing
- **SQL Errors**: Safe execution with error reporting
- **Network Issues**: Graceful handling of API and data download failures
- **Invalid Queries**: Prevents dangerous SQL operations

## Security

- **SQL Injection Protection**: Blocks dangerous SQL keywords
- **Read-Only Operations**: Only SELECT queries are allowed
- **API Key Safety**: Uses environment variables for sensitive data

## Limitations

- Requires OpenAI API key for full AI features
- Currently supports Q1 2025 EDGAR data
- SQL generation quality depends on query complexity
- Rate limits apply based on OpenAI API plan

## Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `requests`: HTTP library for API calls
- `beautifulsoup4`: HTML parsing for SEC documents
- `openai`: OpenAI API client
- `sqlite3`: Database (built-in to Python)

## Troubleshooting

1. **"AI features not available"**: Set the OPENAI_API_KEY environment variable
2. **No data loading**: Check internet connection for SEC data download
3. **Query not working**: Try rephrasing the query or check example queries
4. **SQL errors**: Enable "Show generated SQL queries" to debug

## Future Enhancements

- Support for multiple quarters/years
- Advanced document parsing for more detailed information
- Data visualization capabilities
- Export functionality for query results
- Support for additional LLM providers (Claude, Gemini, etc.)

## Project Structure

```
edgar-query-tool/
├── src/                          # Source code
│   └── edgar_query/             # Main package
│       ├── agents/              # AI agents (SQL generation, execution, etc.)
│       ├── api/                 # FastAPI web service
│       └── web/                 # Web server components
├── data/                        # Data files and database
│   ├── edgar_data/             # Downloaded EDGAR data
│   └── edgar_filings.db        # SQLite database
├── edgar/                       # Main package
│   ├── api/                    # FastAPI server
│   ├── web/                    # Web interface
│   ├── services/               # Business services
│   ├── core/                   # Core business logic
│   └── cli/                    # Command-line interface
├── docs/                        # Documentation
├── tests/                       # Unit tests
├── scripts/                     # Helper scripts
└── pyproject.toml              # Modern Python packaging
```

## Development Setup

For developers who want to contribute or modify the code:

1. Clone the repository and navigate to the project directory

2. Install `uv` if not already installed (see Installation section above)

3. Set up the development environment:
   ```bash
   # Install all dependencies including dev tools
   uv sync --dev
   
   # Set up data directories
   uv run python -c "from pathlib import Path; Path('data/edgar_data').mkdir(parents=True, exist_ok=True); Path('data/backups').mkdir(parents=True, exist_ok=True)"
   ```

4. Set up pre-commit hooks (optional):
   ```bash
   uv run pre-commit install
   ```

5. Run tests:
   ```bash
   uv run pytest tests/
   # With coverage
   uv run pytest tests/ --cov=edgar --cov-report=html
   ```

6. Code quality checks:
   ```bash
   # Lint and format code
   uv run ruff check edgar/ tests/
   uv run ruff format edgar/ tests/
   
   # Type checking
   uv run mypy edgar/
   ```

### UV Commands Reference

```bash
# Project management
uv sync                          # Install dependencies
uv sync --dev                    # Install with dev dependencies
uv add <package>                 # Add new dependency
uv remove <package>              # Remove dependency

# Running code
edgar-api                        # Run API server
edgar-web                        # Run web server
uv run pytest tests/             # Run tests

# Code quality
uv run ruff check edgar/         # Lint code
uv run ruff format edgar/        # Format code
uv run mypy edgar/               # Type checking

# Building
uv build                         # Build package
```
