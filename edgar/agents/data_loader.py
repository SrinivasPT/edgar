import sqlite3
from pathlib import Path

import pandas as pd


class DataLoaderAgent:
    def __init__(self, db_path=None, data_folder=None):
        # Get project root directory (go up from edgar/services/)
        project_root = Path(__file__).parent.parent.parent

        self.db_path = project_root / "data" / "edgar_filings.db"
        self.data_folder = project_root / "data" / "edgar_data"

        self.schema_table_file_path = (
            project_root / "data" / "schema" / "schema_table.sql"
        )
        self.schema_index_file_path = (
            project_root / "data" / "schema" / "schema_index.sql"
        )

        self.master_zip_file = self.data_folder / "master.zip"
        self.master_idx_file = self.data_folder / "master.idx"

        self.sub_file = self.data_folder / "sub.txt"
        self.pre_file = self.data_folder / "pre.txt"

        self.conn = None

        # Create data folder if it doesn't exist
        self.data_folder.mkdir(parents=True, exist_ok=True)

    def init_db(self):
        # Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        if self.db_path.exists():
            print(f"Database already exists at {self.db_path}.")
            self.conn = sqlite3.connect(self.db_path)
            return self.conn

        self.conn = sqlite3.connect(self.db_path)

        with open(self.schema_table_file_path, "r") as schema_file:  # noqa: UP015
            schema_sql = schema_file.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()
            print("Created database schema from schema_table.sql")

        self.load_master_data()
        self.load_sub_data()
        self.load_pre_data()

        with open(self.schema_index_file_path, "r") as schema_file:  # noqa: UP015
            schema_sql = schema_file.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()
            print("Created database schema from schema_index.sql")

        return self.conn

    def load_master_data(self) -> bool:
        if not self.master_idx_file.exists():
            raise FileNotFoundError(
                f"Master index file not found: {self.master_idx_file}"
            )

        print("Loading master index into database...")
        df = pd.read_csv(
            self.master_idx_file,
            sep="|",
            encoding="latin-1",
            skiprows=10,
            names=["cik", "company_name", "form_type", "date_filed", "filename"],
            dtype={
                "cik": str,
                "company_name": str,
                "form_type": str,
                "date_filed": str,
                "filename": str,
            },
            low_memory=False,
        )

        # Convert CIK from string to integer, removing leading zeros
        df["cik"] = pd.to_numeric(df["cik"], errors="coerce").astype("Int64")

        df.to_sql("master_index", self.conn, if_exists="replace", index=False)
        print("Master index loaded into database.")
        return True

    def load_pre_data(self) -> bool:
        """Load pre.txt file containing presentation data."""
        pre_file = self.data_folder / "pre.txt"
        if not pre_file.exists():
            raise FileNotFoundError(f"Pre file not found: {pre_file}")

        df = pd.read_csv(pre_file, sep="\t", dtype=str, low_memory=False)

        df.to_sql(
            "presentation_of_statement", self.conn, if_exists="replace", index=False
        )
        print("Presentation of statement data loaded into database.")
        return True

    def load_sub_data(self) -> bool:
        """Load sub.txt file containing submission data."""
        sub_file = self.data_folder / "sub.txt"

        if not sub_file.exists():
            raise FileNotFoundError(f"Sub file not found: {sub_file}")

        df = pd.read_csv(sub_file, sep="\t", dtype=str, low_memory=False)

        # Convert CIK from string to integer, removing leading zeros
        if "cik" in df.columns:
            df["cik"] = pd.to_numeric(df["cik"], errors="coerce").astype("Int64")

        df.to_sql("submissions", self.conn, if_exists="replace", index=False)
        print("Submission data loaded into database.")
        return True
