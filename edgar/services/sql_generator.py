import os
import re
from pathlib import Path

from openai import OpenAI


class SQLGeneratorService:
    def __init__(self):
        self.openai_client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)

    def get_database_schema_info(self):
        # Get project root directory (go up from edgar/services/)
        project_root = Path(__file__).parent.parent.parent

        # Try multiple possible locations for schema.md
        possible_paths = [
            project_root / "docs" / "schema.md",
            project_root / "schema.md",
            Path("docs/schema.md"),
            Path("schema.md"),
        ]

        for schema_file in possible_paths:
            if schema_file.exists():
                with open(schema_file, encoding="utf-8") as f:
                    return f.read()

        # Return a basic schema if file not found
        return """
        Database Schema:

        Table: filings
        - cik: Company Central Index Key (TEXT)
        - company_name: Company name (TEXT)
        - form_type: SEC form type like 10-K, 10-Q, 8-K (TEXT)
        - date_filed: Filing date in YYYY-MM-DD format (TEXT)
        - filename: Path to filing document (TEXT)
        """

    def normalize_cik_in_query(self, user_query):
        cik_pattern = r"\\b0+(\\d{1,10})\\b"

        def replace_cik(match):
            return match.group(1)

        normalized_query = re.sub(cik_pattern, replace_cik, user_query)
        return normalized_query

    def generate_sql_query(self, user_query):
        if not self.openai_client:
            print("OpenAI API key not configured")
            return None, None
        normalized_query = self.normalize_cik_in_query(user_query)
        schema = self.get_database_schema_info()
        prompt = f"""
        You are a SQL expert. Given the database schema and user query, generate a precise SQL query.

        {schema}

        User Query: {normalized_query}

        Rules based on the schema above:
        1. Only return the SQL query, no explanations
        2. Use proper SQL syntax for SQLite
        3. **Use COUNT(*) for counting only. For other queries, return the full data.**
        4. Return only SELECT statements
        5. Use LIKE for partial matches with % wildcards
        6. For company names, always use UPPER(company_name) LIKE '%SEARCHTERM%' for case-insensitive partial matches
        7. For form types, always identify and convert the user-entered value to the closest standard form type used in the database (e.g., map '24-F' to '24F', '10 K' to '10-K', etc.), then if the form type may have variants, use form_type LIKE 'STANDARD%' to match all related types
        8. Follow the CIK handling and company name matching rules specified in the schema
        9. Use the query patterns provided in the schema as examples
          SQL Query:
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a SQL expert that generates precise SQLite queries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
            )
            if response.choices and response.choices[0].message.content:
                sql_query = response.choices[0].message.content.strip()
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                print(f"Generated SQL Query: {sql_query}")
                return sql_query, prompt
            else:
                print("No response received from OpenAI API")
                return None, prompt

        except Exception as e:
            print(f"Error generating SQL: {e}")
            return None, prompt
