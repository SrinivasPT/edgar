import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    conn = sqlite3.connect(db_path)

    # Create test tables
    conn.execute(
        """
        CREATE TABLE filings (
            cik INTEGER,
            company_name TEXT,
            form_type TEXT,
            date_filed TEXT,
            filename TEXT
        )
    """
    )

    # Insert test data
    test_data = [
        ("123456789", "Test Company Inc", "10-K", "2025-01-15", "test1.htm"),
        ("987654321", "Another Corp", "10-Q", "2025-02-15", "test2.htm"),
        ("111111111", "Third Company", "8-K", "2025-03-15", "test3.htm"),
    ]

    conn.executemany("INSERT INTO filings VALUES (?, ?, ?, ?, ?)", test_data)
    conn.commit()

    yield conn

    conn.close()
    Path(db_path).unlink()


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
