import sqlite3
import zipfile
from pathlib import Path

import pandas as pd


class DataLoaderAgent:
    def __init__(self, db_path=None, data_folder=None):
        # Get project root directory (go up from src/edgar_query/agents/)
        project_root = Path(__file__).parent.parent.parent.parent

        # Set default paths relative to project root
        if db_path is None:
            db_path = project_root / "data" / "edgar_filings.db"
        if data_folder is None:
            data_folder = project_root / "data" / "edgar_data"

        self.db_path = str(db_path)
        self.data_folder = Path(data_folder)
        self.master_zip_file = self.data_folder / "master.zip"
        self.master_idx_file = self.data_folder / "master.idx"
        self.conn = None

        # Create data folder if it doesn't exist
        self.data_folder.mkdir(parents=True, exist_ok=True)

    def init_db(self):
        # Ensure the database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS filings (
                cik TEXT, company_name TEXT, form_type TEXT, date_filed TEXT, filename TEXT
            )
            """
        )
        return self.conn

    def extract_master_index(self):
        if self.master_idx_file.exists():
            print("Master index file already extracted, using cached version")
            return True
        try:
            if not self.master_zip_file.exists():
                print("Master zip file not found")
                return False
            print("Extracting master index file...")
            with zipfile.ZipFile(self.master_zip_file) as z:
                with z.open("master.idx") as idx_file:
                    with open(self.master_idx_file, "wb") as f:
                        f.write(idx_file.read())
            print("Master index file extracted successfully")
            return True
        except Exception as e:
            print(f"Error extracting master index: {e}")
            return False

    def load_master_index(self):
        try:
            if not self.extract_master_index():
                return False
            print("Loading master index into database...")
            df = pd.read_csv(
                self.master_idx_file,
                sep="|",
                encoding="latin-1",
                skiprows=10,
                names=["cik", "company_name", "form_type", "date_filed", "filename"],
            )
            df.to_sql("filings", self.conn, if_exists="replace", index=False)
            print(f"Loaded {len(df)} filings into database")
            return True
        except Exception as e:
            print(f"Error loading master index: {e}")
            return False

    def clear_cached_data(self):
        try:
            if self.master_zip_file.exists():
                self.master_zip_file.unlink()
            if self.master_idx_file.exists():
                self.master_idx_file.unlink()
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
