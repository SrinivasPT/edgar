from edgar_query.agents.sql_executor import SQLExecutorAgent


def test_sql_executor_forbidden_operations(temp_db):
    """Test that forbidden SQL operations are blocked."""
    executor = SQLExecutorAgent(temp_db)

    forbidden_queries = [
        "DROP TABLE filings",
        "DELETE FROM filings",
        "INSERT INTO filings VALUES (1, 'test', 'test', 'test', 'test')",
        "UPDATE filings SET company_name = 'hacked'",
        "CREATE TABLE malicious (id INT)",
        "ALTER TABLE filings ADD COLUMN malicious TEXT",
        "TRUNCATE TABLE filings",
    ]

    for query in forbidden_queries:
        result, error = executor.execute_sql_query(query)
        assert result is None
        assert "forbidden operations" in error.lower()


def test_sql_executor_valid_select(temp_db):
    """Test that valid SELECT queries work."""
    executor = SQLExecutorAgent(temp_db)

    result, error = executor.execute_sql_query("SELECT COUNT(*) as count FROM filings")
    assert error is None
    assert result is not None
    assert len(result) == 1
    assert result.iloc[0]["count"] == 3


def test_sql_executor_invalid_syntax(temp_db):
    """Test handling of invalid SQL syntax."""
    executor = SQLExecutorAgent(temp_db)

    result, error = executor.execute_sql_query("SELECT * FROM nonexistent_table")
    assert result is None
    assert error is not None
    assert "error executing query" in error.lower()
