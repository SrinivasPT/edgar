# EDGAR Filings Database Schema

## Overview
This SQLite database stores SEC EDGAR filing information downloaded from the SEC's quarterly master index files. The database is designed to support natural language queries for SEC filing analysis and research.

## Database Connection
- **File**: `edgar_filings.db` (SQLite 3)
- **Location**: Root directory of the project
- **Connection**: Standard SQLite connection using Python's `sqlite3` module

## Tables

### `filings` Table
The main table containing SEC filing records from the quarterly master index.

**Schema:**
```sql
CREATE TABLE "filings" (
  "cik" TEXT,
  "company_name" TEXT,
  "form_type" TEXT,
  "date_filed" TEXT,
  "filename" TEXT
)
```

**Column Details:**
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `cik` | TEXT | Central Index Key - unique company identifier (WITHOUT leading zeros) | `1000045` |
| `company_name` | TEXT | Company name in UPPERCASE format | `OLD MARKET CAPITAL Corp` |
| `form_type` | TEXT | Type of SEC form filed | `10-K`, `10-Q`, `8-K`, `S-1`, `BD` |
| `date_filed` | TEXT | Filing date in YYYY-MM-DD format | `2025-02-14` |
| `filename` | TEXT | Path to the filing document on SEC servers | `edgar/data/1000045/0000950170-25-021128.txt` |

**Data Characteristics:**
- **Total Records**: ~338,662 filings (Q1 2025 data)
- **CIK Format**: Stored WITHOUT leading zeros (e.g., `1000045` not `0001000045`)
- **Company Names**: All stored in UPPERCASE
- **Date Range**: Current quarter's filings
- **No Primary Key**: Table allows duplicate entries


**standard form_type**
1, 1-A, 1-A/A, 1-A POS, 1-E, 1-E/A, 1-K, 1-SA, 1-U, 1-Z, 2-E, 3, 3/A, 4, 4/A, 5, 5/A, 6-K, 6-K/A, 8-A, 8-A/A, 8-B, 8-B/A, 8-K, 8-K/A, 8-K12B, 8-K12B/A, 8-K12G3, 8-K12G3/A, 8-K15D5, 8-K15D5/A, 10, 10/A, 10-C, 10-C/A, 10-D, 10-D/A, 10-K, 10-K/A, 10-KT, 10-KT/A, 10-Q, 10-Q/A, 10-QT, 10-QT/A, 11-K, 11-K/A, 13F-HR, 13F-HR/A, 13F-NT, 13F-NT/A, 15, 15/A, 15F, 15F/A, 18, 18/A, 18-K, 18-K/A, 20-F, 20-F/A, 24F-2NT, 24F-2NT/A, 25, 25/A, 25-NSE, 25-NSE/A, 40-17F1, 40-17F1/A, 40-17F2, 40-17F2/A, 40-17G, 40-17G/A, 40-202A, 40-202A/A, 40-206A, 40-206A/A, 40-APP, 40-APP/A, 40-F, 40-F/A, 40-OIP, 40-OIP/A, 48B-2NT, 48B-2NT/A, 144, 144/A, 425, 425/A, ABS-15G, ABS-15G/A, ABS-EE, ABS-EE/A, ARS, ARS/A, CB, CB/A, CFPORTAL, CFPORTAL/A, D, D/A, DEF 14A, DEF 14A/A, DEF 14C, DEF 14C/A, DEFA14A, DEFA14A/A, DEFM14A, DEFM14A/A, DEFM14C, DEFM14C/A, F-1, F-1/A, F-1MEF, F-3, F-3/A, F-3D, F-3D/A, F-3DPOS, F-3DPOS/A, F-4, F-4/A, F-4MEF, F-6, F-6/A, F-6 POS, F-7, F-7/A, F-8, F-8/A, F-10, F-10/A, F-10MEF, F-80, F-80/A, F-N, F-N/A, F-X, F-X/A, MA, MA/A, MA-I, MA-I/A, MA-W, N-1A, N-1A/A, N-2, N-2/A, N-2MEF, N-3, N-3/A, N-4, N-4/A, N-5, N-5/A, N-6, N-6/A, N-8B-2, N-8B-2/A, N-8B-4, N-8B-4/A, N-8F, N-8F/A, N-14, N-14/A, N-14MEF, N-CEN, N-CEN/A, N-CSR, N-CSR/A, N-MFP, N-MFP/A, N-PX, N-PX/A, N-Q, N-Q/A, NT 10-D, NT 10-D/A, NT 10-K, NT 10-K/A, NT 10-Q, NT 10-Q/A, NT 11-K, NT 11-K/A, NT 15D2, NT 15D2/A, NT 20-F, NT 20-F/A, NT-NCSR, NT-NCSR/A, POS AM, POS AM/A, POS EX, POS EX/A, POS462B, POS462B/A, POS462C, POS462C/A, PRE 14A, PRE 14A/A, PRE 14C, PRE 14C/A, PREM14A, PREM14A/A, PREM14C, PREM14C/A, S-1, S-1/A, S-1MEF, S-2, S-2/A, S-2MEF, S-3, S-3/A, S-3ASR, S-3D, S-3D/A, S-3DPOS, S-3DPOS/A, S-4, S-4/A, S-4MEF, S-6, S-6/A, S-8, S-8/A, S-8 POS, S-11, S-11/A, S-11MEF, S-20, S-20/A, SBSE, SBSE/A, SBSE-A, SBSE-A/A, SBSE-BD, SBSE-BD/A, SBSE-C, SBSE-C/A, SC 13D, SC 13D/A, SC 13E1, SC 13E1/A, SC 13E3, SC 13E3/A, SC 13G, SC 13G/A, SC 14D1, SC 14D1/A, SC 14D9, SC 14D9/A, SC 14F1, SC 14F1/A, SC TO-C, SC TO-C/A, SC TO-I, SC TO-I/A, SC TO-T, SC TO-T/A, SD, SD/A, SF-1, SF-1/A, SF-1MEF, SF-3, SF-3/A, SP 15D2, SP 15D2/A, T-3, T-3/A, TA-1, TA-1/A, TA-2, TA-2/A, TA-W, UNDER, UNDER/A, X-17A-5, X-17A-5/A

## Query Patterns

### CIK Searches
```sql
-- Direct CIK lookup (no leading zeros)
SELECT * FROM filings WHERE cik = '1000045';

-- Partial CIK match
SELECT * FROM filings WHERE cik LIKE '100004%';
```

### Company Name Searches
```sql
-- Case-insensitive company search
SELECT * FROM filings WHERE UPPER(company_name) LIKE '%APPLE%';
```

### Form Type Filtering
```sql
-- Specific form type
SELECT * FROM filings WHERE form_type = '10-K';

-- Multiple form types
SELECT * FROM filings WHERE form_type IN ('10-K', '10-Q');
```

### Date Filtering
```sql
-- Recent filings
SELECT * FROM filings WHERE date_filed >= '2025-03-01';

-- Date range
SELECT * FROM filings WHERE date_filed BETWEEN '2025-01-01' AND '2025-03-31';
```

## Important Notes for Natural Language Processing

### CIK Handling
- **Database Storage**: CIKs stored WITHOUT leading zeros
- **User Input**: May include leading zeros (e.g., `0001000045`)
- **Normalization Required**: Remove leading zeros before querying
- **Example**: `0001000045` → `1000045`

### Company Name Matching
- **Case Sensitivity**: Always use `UPPER()` function for case-insensitive searches
- **Partial Matching**: Use `LIKE '%TERM%'` for substring matches
- **Example**: `UPPER(company_name) LIKE '%MICROSOFT%'`

### Security Constraints
The application restricts SQL operations to SELECT statements only. The following operations are forbidden:
- `DROP`, `DELETE`, `INSERT`, `UPDATE`
- `CREATE`, `ALTER`, `TRUNCATE`

## Performance Considerations
- **No Indexes**: Currently no indexes defined (consider adding for better performance)
- **Large Dataset**: ~338K records require efficient queries
- **Recommended Indexes**:
  ```sql
  CREATE INDEX idx_cik ON filings(cik);
  CREATE INDEX idx_form_type ON filings(form_type);
  CREATE INDEX idx_date_filed ON filings(date_filed);
  CREATE INDEX idx_company_name ON filings(company_name);
  ```

## Usage Context
This schema is used by a Streamlit application that:
1. Downloads SEC master index files
2. Loads filing data into SQLite
3. Accepts natural language queries
4. Converts queries to SQL using LLM
5. Returns formatted results

The database serves as the foundation for SEC filing research and analysis tools.