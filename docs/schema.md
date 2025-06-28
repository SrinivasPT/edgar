# Instructions for LLM to Generate SQL Queries for EDGAR Filings Database

## Objective
Generate SQL `SELECT` queries dynamically for the `edgar_filings.db` SQLite database using data from `master.idx`, `pre.txt`, and `sub.txt` files. The queries should support natural language analysis of SEC EDGAR filings, addressing queries related to registration status, company metadata, filing history, audit/compliance, and advanced filtering/export. The database includes the `master_index`, `submissions`, and `presentation_of_statement` tables.

## Database Overview
- **Database File**: `edgar_filings.db` (SQLite 3)
- **Tables**: `master_index`, `submissions`, `presentation_of_statement`
- **Purpose**: Store and query SEC filing data for research, analysis, and compliance
- **Constraints**: Only `SELECT` statements are allowed; `DROP`, `DELETE`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `TRUNCATE` are prohibited
- **Current Date**: Queries should assume the current date is June 28, 2025, unless specified otherwise

## Input Data Files
The following files from the EDGAR financial statements dataset provide the data to construct queries:

1. **master.idx**:
   - Contains quarterly SEC filing records.
   - Fields: `CIK`, `Company Name`, `Form Type`, `Date Filed`, `Filename`.
   - Maps to the `master_index` table.
   - Example: `1000045|OLD MARKET CAPITAL Corp|10-K|2025-02-14|edgar/data/1000045/0000950170-25-021128.txt`

2. **sub.txt**:
   - Contains detailed submission metadata.
   - Fields: `adsh`, `cik`, `name`, `sic`, `form`, `period`, `filed`, `fy`, `fp`, `countryba`, `stprba`, `cityba`, `afs`, `wksi`, etc.
   - Maps to the `submissions` table.
   - Example: `0000012345-25-000001|1000045|Apple Inc.|3571|10-K|20241231|20250214|2024|FY`

3. **pre.txt**:
   - Contains financial statement presentation data.
   - Fields: `adsh`, `report`, `line`, `stmt`, `tag`, `plabel`, `version`, etc.
   - Maps to the `presentation_of_statement` table.
   - Example: `0000012345-25-000001|1|100|BS|Assets|Total Assets|us-gaap/2023`

## Database Schema

### 1. `master_index` Table
Stores SEC filing records from `master.idx`.

**Schema**:
```sql
CREATE TABLE master_index (
    cik TEXT,
    company_name TEXT,
    form_type TEXT,
    date_filed TEXT,
    filename TEXT
)
```

**Key Details**:
- `cik`: Company identifier (TEXT, no leading zeros, e.g., `1000045`)
- `company_name`: UPPERCASE company name (e.g., `OLD MARKET CAPITAL Corp`)
- `form_type`: SEC form type (e.g., `10-K`, `10-Q`, `8-K`, `13F-HR`)
- `date_filed`: Filing date (YYYY-MM-DD, e.g., `2025-02-14`)
- `filename`: Path to filing document (e.g., `edgar/data/1000045/0000950170-25-021128.txt`)
- **Notes**: No primary key; allows duplicates; ~338,662 records for Q1 2025.

### 2. `submissions` Table
Stores submission metadata from `sub.txt`.

**Schema** (Partial):
```sql
CREATE TABLE submissions (
    adsh TEXT(20) NOT NULL PRIMARY KEY,
    cik INTEGER NOT NULL,
    name TEXT(150) NOT NULL,
    sic INTEGER,
    form TEXT(10),
    period TEXT(8),
    filed TEXT(8),
    accepted TEXT(19),
    fy INTEGER,
    fp TEXT(2),
    countryba TEXT,
    stprba TEXT,
    cityba TEXT,
    zipba TEXT,
    bas1 TEXT,
    bas2 TEXT,
    countryinc TEXT,
    ein TEXT,
    afs TEXT,
    wksi INTEGER
)
```

**Key Details**:
- `adsh`: Accession number (e.g., `0000012345-25-000001`)
- `cik`: Company identifier (INTEGER, e.g., `1000045`)
- `name`: Company name (e.g., `Apple Inc.`)
- `sic`: Standard Industrial Classification code (e.g., `3571` for Electronic Computers)
- `form`: Submission type (e.g., `10-K`, `13F-HR`)
- `period`: Balance sheet date (YYYYMMDD, e.g., `20241231`)
- `filed`: Filing date (YYYYMMDD, e.g., `20250214`)
- `fy`: Fiscal year (e.g., `2024`)
- `fp`: Fiscal period (e.g., `FY`, `Q1`)
- `countryba`, `stprba`, `cityba`, `zipba`, `bas1`, `bas2`: Business address fields
- `afs`: Filer status (e.g., `LAF`, `ACC`, `SRA`, `NON`, `SML`)
- `wksi`: Well Known Seasoned Issuer (0 or 1)
- **Notes**: `sic` codes starting with `60` indicate financial firms (e.g., `6021` for National Commercial Banks); tech sector typically includes `3570-3579`, `3600-3699`, `7370-7379`.

### 3. `presentation_of_statement` Table
Stores financial statement presentation data from `pre.txt`.

**Schema** (Partial):
```sql
CREATE TABLE presentation_of_statement (
    adsh TEXT(20) NOT NULL,
    report INTEGER NOT NULL,
    line INTEGER NOT NULL,
    stmt TEXT(2) NOT NULL,
    tag TEXT(256),
    plabel TEXT(512),
    version TEXT(20),
    PRIMARY KEY (adsh, report, line),
    FOREIGN KEY (adsh) REFERENCES submissions(adsh)
)
```

**Key Details**:
- `adsh`: Accession number (links to `submissions`)
- `report`: Report grouping (e.g., `1`)
- `line`: Presentation order (e.g., `100`)
- `stmt`: Statement type (e.g., `BS` for Balance Sheet, `IS` for Income Statement)
- `tag`: Line item tag (e.g., `Assets`)
- `plabel`: Preferred label (e.g., `Total Assets`)

## Table Relationships
- **Join `master_index` and `submissions`**:
  - Use `CAST(submissions.cik AS TEXT) = master_index.cik` due to different data types.
- **Join `submissions` and `presentation_of_statement`**:
  - Use `presentation_of_statement.adsh = submissions.adsh`.

## Guidelines for Query Generation

### 1. General Principles
- Generate only `SELECT` queries to comply with security constraints.
- Use table aliases (`m` for `master_index`, `s` for `submissions`, `p` for `presentation_of_statement`) for readability.
- Optimize queries for a large dataset (~338K records in `master_index`).
- Handle user inputs dynamically based on natural language requests.
- For export requests (e.g., JSON), structure query results to include relevant metadata fields.

### 2. Handling Input Data
- **CIK**:
  - Remove leading zeros from `master.idx` CIK values (e.g., `0001000045` → `1000045`).
  - Convert `submissions.cik` to TEXT when joining with `master_index`.
- **Company Name**:
  - Use `UPPER()` for case-insensitive searches in `master_index.company_name`.
  - Support partial matches with `LIKE '%TERM%'`.
  - Use `submissions.name` for more accurate names when available.
- **Form Type**:
  - Validate against standard form types (e.g., `10-K`, `10-Q`, `8-K`, `13F-HR`).
  - Use `IN` for multiple form types (e.g., `form_type IN ('10-K', '8-K')`).
- **Date Fields**:
  - Convert `submissions.filed` and `submissions.period` (YYYYMMDD) to YYYY-MM-DD for comparisons with `master_index.date_filed`.
  - Use SQLite date functions (e.g., `date(substr(s.filed, 1, 4) || '-' || substr(s.filed, 5, 2) || '-' || substr(s.filed, 7, 2))`) for formatting.
- **SIC Codes**:
  - Filter by specific codes or ranges (e.g., `sic BETWEEN 3570 AND 3579` for tech, `sic LIKE '60%'` for financial firms).
  - Healthcare sector typically includes `sic` codes `8000-8099`.
- **Registration Status**:
  - Infer Section 12 or 15 registration from `submissions.afs` (filer status) and `submissions.wksi`.
  - Assume `afs` values like `LAF` (Large Accelerated Filer), `ACC` (Accelerated Filer), or `SRA` (Smaller Reporting Accelerated) indicate Section 12 registration.
  - Section 15 registration may apply to broker-dealers (form types like `SBSE`, `SBSE-A`).
- **13F Threshold**:
  - Identify 13F filers via `form_type = '13F-HR'` or `form_type = '13F-NT'`.
  - Threshold crossing requires comparing filing dates to the previous quarter.

### 3. Query Patterns
The LLM should generate queries tailored to the following categories, using data from `master.idx`, `sub.txt`, and `pre.txt`:

#### a. Registration Status & 13F Threshold
**Examples**:
1. **Is XYZ Corporation registered under Section 12 or 15?**
   ```sql
   SELECT s.name, s.cik, s.afs, s.wksi, m.form_type
   FROM submissions s
   LEFT JOIN master_index m ON CAST(s.cik AS TEXT) = m.cik
   WHERE UPPER(s.name) LIKE '%XYZ CORPORATION%'
     AND (s.afs IN ('LAF', 'ACC', 'SRA') OR m.form_type LIKE 'SBSE%')
   LIMIT 1;
   ```
   - **Logic**: Check `afs` for Section 12 (e.g., `LAF`, `ACC`) and `form_type` for Section 15 (e.g., `SBSE`). Use latest submission.

2. **List all companies registered under Section 15 as of June 2025**
   ```sql
   SELECT DISTINCT s.name, s.cik, m.form_type, m.date_filed
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type LIKE 'SBSE%'
     AND m.date_filed <= '2025-06-30'
   ORDER BY s.name;
   ```
   - **Logic**: Filter for `SBSE` form types indicating broker-dealer (Section 15) registration.

3. **Which companies in the tech sector crossed the 13F threshold last quarter?**
   ```sql
   SELECT DISTINCT s.name, s.cik, m.form_type, m.date_filed
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type IN ('13F-HR', '13F-NT')
     AND m.date_filed BETWEEN '2025-01-01' AND '2025-03-31'
     AND s.sic BETWEEN 3570 AND 3579
   ORDER BY m.date_filed;
   ```
   - **Logic**: Identify new 13F filers in Q1 2025 (Jan-Mar) with tech SIC codes.

**LLM Guidance**:
- Use `afs` and `wksi` for Section 12; check `form_type` for Section 15.
- For 13F, filter by `13F-HR` or `13F-NT` and compare filing dates across quarters.
- Restrict to relevant date ranges (e.g., `date_filed` or `filed`).

#### b. Company Metadata Lookup
**Examples**:
1. **What is the SIC code and business address for ABC Holding?**
   ```sql
   SELECT s.name, s.cik, s.sic, s.countryba, s.stprba, s.cityba, s.zipba, s.bas1, s.bas2
   FROM submissions s
   WHERE UPPER(s.name) LIKE '%ABC HOLDING%'
   LIMIT 1;
   ```
   - **Logic**: Retrieve latest submission record for address and SIC.

2. **Show the executive team listed in the latest 10-K filing for ABC Inc.**
   ```sql
   SELECT s.name, s.cik, m.form_type, m.date_filed, m.filename
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE UPPER(s.name) LIKE '%ABC INC%'
     AND m.form_type = '10-K'
   ORDER BY m.date_filed DESC
   LIMIT 1;
   ```
   - **Logic**: Identify latest 10-K; note that executive team data may require parsing `filename` content (not directly in database).

3. **Retrieve the CIK and registration status for all companies filed in the last 7 days**
   ```sql
   SELECT DISTINCT s.name, s.cik, s.afs, s.wksi
   FROM submissions s
   WHERE date(substr(s.filed, 1, 4) || '-' || substr(s.filed, 5, 2) || '-' || substr(s.filed, 7, 2)) >= date('2025-06-28', '-7 days')
   ORDER BY s.name;
   ```
   - **Logic**: Filter by `filed` date within 7 days; use `afs` for registration status.

**LLM Guidance**:
- Use `submissions` for metadata like `sic`, `countryba`, `stprba`.
- For executive data, return `filename` or suggest external parsing of 10-K filings.
- Convert `filed` (YYYYMMDD) to YYYY-MM-DD for date filtering.

#### c. Filing History & Trends
**Examples**:
1. **How many 10-K filings submitted by financial firms in Q1 2025?**
   ```sql
   SELECT COUNT(*) AS filing_count
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type = '10-K'
     AND m.date_filed BETWEEN '2025-01-01' AND '2025-03-31'
     AND s.sic LIKE '60%';
   ```
   - **Logic**: Count 10-K filings for financial firms (SIC `60xx`).

2. **List all companies that changed their registration status in the past year**
   ```sql
   SELECT s.name, s.cik, s.afs, s.filed
   FROM submissions s
   WHERE s.filed >= '20240628'
     AND s.afs IS NOT NULL
   ORDER BY s.name, s.filed;
   ```
   - **Logic**: Compare `afs` across submissions; requires manual analysis of changes (not directly trackable).

3. **Which companies filed both 10-K and 8-K in the last 30 days?**
   ```sql
   SELECT s.name, s.cik
   FROM submissions s
   JOIN master_index m ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type IN ('10-K', '8-K')
     AND m.date_filed >= date('2025-06-28', '-30 days')
   GROUP BY s.cik, s.name
   HAVING COUNT(DISTINCT m.form_type) = 2;
   ```
   - **Logic**: Use `GROUP BY` and `HAVING` to ensure both form types exist.

**LLM Guidance**:
- Use `COUNT`, `GROUP BY`, and date ranges for trends.
- For status changes, suggest comparing `afs` across time (may require external logic).
- Validate form types and SIC ranges.

#### d. Audit & Compliance Checks
**Examples**:
1. **Highlight discrepancies between Bloomberg 13F and EDGAR-derived registration status**
   ```sql
   SELECT s.name, s.cik, s.afs, m.form_type, m.date_filed
   FROM submissions s
   LEFT JOIN master_index m ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type IN ('13F-HR', '13F-NT')
     AND s.afs NOT IN ('LAF', 'ACC', 'SRA')
     AND m.date_filed <= '2025-06-30';
   ```
   - **Logic**: Identify 13F filers without expected registration status.

2. **Generate report of all companies missing registration status**
   ```sql
   SELECT s.name, s.cik
   FROM submissions s
   WHERE s.afs IS NULL
   ORDER BY s.name;
   ```
   - **Logic**: Filter for `NULL` `afs` values.

3. **Which companies have not filed a 10-K in the past 12 months?**
   ```sql
   SELECT DISTINCT s.name, s.cik
   FROM submissions s
   LEFT JOIN master_index m ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type = '10-K'
     AND (m.date_filed < '2024-06-28' OR m.date_filed IS NULL)
   ORDER BY s.name;
   ```
   - **Logic**: Identify companies without recent 10-K filings.

**LLM Guidance**:
- For discrepancies, compare `form_type` (e.g., 13F) with `afs`.
- Handle `NULL` values explicitly for missing data.
- Use `LEFT JOIN` to find non-filers.

#### e. Advanced Filtering & Export
**Examples**:
1. **Export all Section 12 registered companies in the healthcare sector**
   ```sql
   SELECT s.name, s.cik, s.afs, s.sic, s.countryba, s.stprba, s.cityba
   FROM submissions s
   WHERE s.afs IN ('LAF', 'ACC', 'SRA')
     AND s.sic BETWEEN 8000 AND 8099
   ORDER BY s.name;
   ```
   - **Logic**: Filter by `afs` and healthcare SIC codes; structure for JSON export.

2. **Show all filings with executive changes and export metadata to JSON**
   ```sql
   SELECT s.name, s.cik, m.form_type, m.date_filed, m.filename
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type = '8-K'
     AND m.date_filed <= '2025-06-30'
   ORDER BY m.date_filed DESC;
   ```
   - **Logic**: Assume 8-K filings may indicate executive changes; include metadata for export.

3. **List all companies with SIC code starting with 60 and registered under Section 12**
   ```sql
   SELECT s.name, s.cik, s.afs, s.sic
   FROM submissions s
   WHERE s.afs IN ('LAF', 'ACC', 'SRA')
     AND s.sic LIKE '60%'
   ORDER BY s.name;
   ```
   - **Logic**: Filter by financial SIC codes and Section 12 status.

**LLM Guidance**:
- For exports, include key metadata fields (e.g., `name`, `cik`, `form_type`, `date_filed`).
- Use `DISTINCT` to avoid duplicates in results.
- Structure results for JSON by selecting clear, relevant columns.

### 4. Error Handling
- **Invalid CIK**: Strip leading zeros; validate format.
- **Unknown Form Type**: Suggest valid form types (e.g., `10-K`, `13F-HR`).
- **Date Mismatch**: Normalize YYYYMMDD to YYYY-MM-DD; handle invalid dates.
- **No Results**: Return “No matching records found” with context (e.g., “No 10-K filings for ABC Inc. in 2025”).
- **Missing Data**: Use `COALESCE` or check for `NULL` in critical fields like `afs`.

### 5. Performance Optimization
- Filter on specific columns (e.g., `cik`, `form_type`, `date_filed`) to reduce scans.
- Use `LIMIT` (e.g., `LIMIT 100`) for large result sets.
- Suggest indexes for performance:
  ```sql
  CREATE INDEX idx_master_cik ON master_index(cik);
  CREATE INDEX idx_master_form_type ON master_index(form_type);
  CREATE INDEX idx_submissions_cik ON submissions(cik);
  CREATE INDEX idx_submissions_adsh ON submissions(adsh);
  CREATE INDEX idx_presentation_adsh ON presentation_of_statement(adsh);
  ```

## Example LLM Workflow
**User Input**: “List all tech companies that filed a 13F-HR in Q1 2025.”
**Steps**:
1. Identify entities:
   - Sector: Tech (`sic BETWEEN 3570 AND 3579`)
   - Form: `13F-HR`
   - Timeframe: Q1 2025 (`date_filed BETWEEN '2025-01-01' AND '2025-03-31'`)
2. Construct query:
   ```sql
   SELECT DISTINCT s.name, s.cik, m.form_type, m.date_filed
   FROM master_index m
   JOIN submissions s ON CAST(s.cik AS TEXT) = m.cik
   WHERE m.form_type = '13F-HR'
     AND m.date_filed BETWEEN '2025-01-01' AND '2025-03-31'
     AND s.sic BETWEEN 3570 AND 3579
   ORDER BY s.name
   LIMIT 100;
   ```
3. Validate:
   - Confirm `13F-HR` is valid.
   - Ensure date range and SIC codes are correct.
   - Handle potential `NULL` SIC values.

## Notes for LLM
- **Context Awareness**: Use conversation history to refine queries (e.g., reuse CIK from prior input).
- **Flexibility**: Support variations (e.g., “Apple Inc.”, “Apple”, CIK `320193`).
- **Export Handling**: For JSON exports, suggest fields like `name`, `cik`, `form_type`, `date_filed`.
- **Limitations**:
  - Executive team data requires parsing filing documents (not in database).
  - Registration status changes need external comparison logic.
  - Bloomberg 13F data is external; compare only with EDGAR `form_type` and `afs`.
- **Memory Management**: If users request to forget chats, instruct them to:
  - Click the book icon under the message and select the chat to forget.
  - Disable memory in the “Data Controls” section of settings.

## Security Reminder
- Restrict to `SELECT` queries only.
- Sanitize inputs to prevent SQL injection (e.g., escape special characters).