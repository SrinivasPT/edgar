# Instructions for LLM to Generate SQL Queries for EDGAR Filings Database

## Objective
Generate SQL `SELECT` queries dynamically for the `edgar_filings.db` SQLite database using data from `master.idx`, `pre.txt`, and `sub.txt` files. The queries should support natural language analysis of SEC EDGAR filings, addressing queries related to registration status, company metadata, filing history, audit/compliance, and advanced filtering/export. The database includes the `master_index`, `submissions`, and `presentation_of_statement` tables. Queries must always use `master_index` as the driving table, as it contains all SEC filing records, while `submissions` and `presentation_of_statement` only include data for companies that filed through XBRL.

## Database Overview
- **Database File**: `edgar_filings.db` (SQLite 3)
- **Tables**: `master_index`, `submissions`, `presentation_of_statement`
- **Purpose**: Store and query SEC filing data for research, analysis, and compliance
- **Constraints**: Only `SELECT` statements are allowed; `DROP`, `DELETE`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `TRUNCATE` are prohibited
- **Current Date**: Queries should assume the current date is June 28, 2025, unless specified otherwise

## Input Data Files
The following files from the EDGAR financial statements dataset provide the data to construct queries:

1. **master.idx**:
   - Contains quarterly SEC filing records for all filings.
   - Fields: `CIK`, `Company Name`, `Form Type`, `Date Filed`, `Filename`.
   - Maps to the `master_index` table.
   - Example: `1000045|OLD MARKET CAPITAL Corp|10-K|2025-02-14|edgar/data/1000045/0000950170-25-021128.txt`

2. **sub.txt**:
   - Contains detailed submission metadata for XBRL filings.
   - Fields: `adsh`, `cik`, `name`, `sic`, `form`, `period`, `filed`, `fy`, `fp`, `countryba`, `stprba`, `cityba`, `afs`, `wksi`, etc.
   - Maps to the `submissions` table.
   - Example: `0000012345-25-000001|1000045|Apple Inc.|3571|10-K|20241231|20250214|2024|FY`

3. **pre.txt**:
   - Contains financial statement presentation data for XBRL filings.
   - Fields: `adsh`, `report`, `line`, `stmt`, `tag`, `plabel`, `version`, etc.
   - Maps to the `presentation_of_statement` table.
   - Example: `0000012345-25-000001|1|100|BS|Assets|Total Assets|us-gaap/2023`

## Database Schema

### 1. `master_index` Table
Stores SEC filing records from `master.idx`.

**Schema**:
```sql
CREATE TABLE master_index (
    cik INTEGER,
    company_name TEXT,
    form_type TEXT,
    date_filed TEXT,
    filename TEXT
)
```

**Key Details**:
- `cik`: Company identifier (INTEGER, no leading zeros, e.g., `1000045`)
- `company_name`: UPPERCASE company name (e.g., `OLD MARKET CAPITAL Corp`)
- `form_type`: SEC form type (e.g., `10-K`, `10-Q`, `8-K`, `13F-HR`)
- `date_filed`: Filing date (YYYY-MM-DD, e.g., `2025-02-14`)
- `filename`: Path to filing document (e.g., `edgar/data/1000045/0000950170-25-021128.txt`)
- **Notes**: No primary key; allows duplicates; ~338,662 records for Q1 2025; includes all filings.

### 2. `submissions` Table
Stores submission metadata from `sub.txt` for XBRL filings.

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
- **Notes**: Only includes XBRL filings; `sic` codes starting with `60` indicate financial firms (e.g., `6021` for National Commercial Banks); tech sector typically includes `3570-3579`, `3600-3699`, `7370-7379`.

### 3. `presentation_of_statement` Table
Stores financial statement presentation data from `pre.txt` for XBRL filings.

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
- **Notes**: Only includes XBRL filings.

## Table Relationships
- **Join `master_index` and `submissions`**:
  - Use `submissions.cik = master_index.cik` for direct INTEGER-to-INTEGER joins.
  - Use `LEFT JOIN` with `master_index` as the driving table to include all filings, as `submissions` may not have entries for non-XBRL filings.
- **Join `submissions` and `presentation_of_statement`**:
  - Use `presentation_of_statement.adsh = submissions.adsh`.
  - Ensure `submissions` is joined to `master_index` first, maintaining `master_index` as the driving table.

## Guidelines for Query Generation

### 1. General Principles
- Generate only `SELECT` queries to comply with security constraints.
- Use table aliases (`m` for `master_index`, `s` for `submissions`, `p` for `presentation_of_statement`) for readability.
- Always use `master_index` as the driving table in all queries, as it contains all SEC filing records, while `submissions` and `presentation_of_statement` are limited to XBRL filings.
- Use `LEFT JOIN` when joining `master_index` with `submissions` or `presentation_of_statement` to ensure all `master_index` records are included, even if no corresponding XBRL data exists.
- Optimize queries for a large dataset (~338K records in `master_index`).
- Handle user inputs dynamically based on natural language requests.
- Include key columns from all relevant tables (e.g., `m.cik`, `m.company_name`, `m.form_type`, `m.date_filed`, `s.name`, `s.sic`, `s.afs`) to provide comprehensive data for LLM processing.
- For export requests (e.g., JSON), structure query results to include relevant metadata fields.

### 2. Handling Input Data
- **CIK**:
  - Remove leading zeros from `master.idx` CIK values during data loading (e.g., `0001000045` → `1000045`).
  - Both tables now use INTEGER type for direct joins.
- **Company Name**:
  - Use `UPPER()` for case-insensitive searches in `master_index.company_name`.
  - Support partial matches with `LIKE '%TERM%'`.
  - Optionally use `submissions.name` for more accurate names, but prioritize `master_index` filters.
- **Form Type**:
  - Validate against standard form types (e.g., `10-K`, `10-Q`, `8-K`, `13F-HR`).
  - Use `IN` for multiple form types (e.g., `form_type IN ('10-K', '8-K')`).
- **Date Fields**:
  - Use `master_index.date_filed` (YYYY-MM-DD) as the primary date filter.
  - Convert `submissions.filed` (YYYYMMDD) to YYYY-MM-DD for comparisons using SQLite date functions (e.g., `date(substr(s.filed, 1, 4) || '-' || substr(s.filed, 5, 2) || '-' || substr(s.filed, 7, 2))`).
- **SIC Codes**:
  - Filter by specific codes or ranges in `submissions.sic` (e.g., `sic BETWEEN 3570 AND 3579` for tech, `sic LIKE '60%'` for financial firms).
  - Healthcare sector typically includes `sic` codes `8000-8099`.
  - Handle `NULL` SIC values, as `submissions` may not exist for all `master_index` records.
- **Registration Status**:
  - Infer Section 12 or 15 registration from `submissions.afs` (filer status) and `submissions.wksi`.
  - Assume `afs` values like `LAF` (Large Accelerated Filer), `ACC` (Accelerated Filer), or `SRA` (Smaller Reporting Accelerated) indicate Section 12 registration.
  - Section 15 registration may apply to broker-dealers (form types like `SBSE`, `SBSE-A` in `master_index.form_type`).
- **13F Threshold**:
  - Identify 13F filers via `master_index.form_type = '13F-HR'` or `form_type = '13F-NT'`.
  - Threshold crossing requires comparing `master_index.date_filed` across quarters.

### 3. Query Patterns
The LLM should generate queries tailored to the following categories, using `master_index` as the driving table and data from `master.idx`, `sub.txt`, and `pre.txt`:

#### a. Registration Status & 13F Threshold
**Examples**:
1. **Is XYZ Corporation registered under Section 12 or 15?**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.afs, s.wksi
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE UPPER(m.company_name) LIKE '%XYZ CORPORATION%'
     AND (s.afs IN ('LAF', 'ACC', 'SRA') OR m.form_type LIKE 'SBSE%')
   ORDER BY m.date_filed DESC
   LIMIT 1;
   ```
   - **Logic**: Start with `master_index`; check `s.afs` for Section 12 and `m.form_type` for Section 15.

2. **List all companies registered under Section 15 as of June 2025**
   ```sql
   SELECT DISTINCT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type LIKE 'SBSE%'
     AND m.date_filed <= '2025-06-30'
   ORDER BY m.company_name;
   ```
   - **Logic**: Use `master_index` to filter `SBSE` forms; include `submissions` for name.

3. **Which companies in the tech sector crossed the 13F threshold last quarter?**
   ```sql
   SELECT DISTINCT m.cik, m.company_name, m.form_type, m.date_filed, s.sic
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type IN ('13F-HR', '13F-NT')
     AND m.date_filed BETWEEN '2025-01-01' AND '2025-03-31'
     AND (s.sic BETWEEN 3570 AND 3579 OR s.sic IS NULL)
   ORDER BY m.date_filed;
   ```
   - **Logic**: Drive with `master_index` for 13F forms; filter tech SIC codes in `submissions`.

**LLM Guidance**:
- Start queries with `FROM master_index m`.
- Use `LEFT JOIN` to include `submissions` data if available.
- Filter registration status using `s.afs` and `m.form_type`.
- Handle `NULL` `submissions` data for non-XBRL filers.

#### b. Company Metadata Lookup
**Examples**:
1. **What is the SIC code and business address for ABC Holding?**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.sic, s.countryba, s.stprba, s.cityba, s.zipba, s.bas1, s.bas2
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE UPPER(m.company_name) LIKE '%ABC HOLDING%'
   ORDER BY m.date_filed DESC
   LIMIT 1;
   ```
   - **Logic**: Drive with `master_index`; include `submissions` for SIC and address.

2. **What is the SIC code for Apple?**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.sic, s.countryba, s.stprba, s.cityba
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE UPPER(m.company_name) LIKE '%APPLE%'
   ORDER BY m.date_filed DESC
   LIMIT 10;
   ```
   - **Logic**: Use `master_index` as driving table; include key `submissions` columns for LLM context.

3. **Show the executive team listed in the latest 10-K filing for ABC Inc.**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE UPPER(m.company_name) LIKE '%ABC INC%'
     AND m.form_type = '10-K'
   ORDER BY m.date_filed DESC
   LIMIT 1;
   ```
   - **Logic**: Drive with `master_index` for 10-K; note executive data requires parsing `filename`.

4. **Retrieve the CIK and registration status for all companies filed in the last 7 days**
   ```sql
   SELECT DISTINCT m.cik, m.company_name, m.form_type, m.date_filed, m.filename,
          s.name, s.afs, s.wksi
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.date_filed >= date('2025-06-28', '-7 days')
   ORDER BY m.company_name;
   ```
   - **Logic**: Use `master_index.date_filed` as primary filter; include `submissions` for status.

**LLM Guidance**:
- Start with `FROM master_index m` for all metadata queries.
- Use `LEFT JOIN` to include `submissions` columns like `sic`, `name`, `countryba`.
- Include all `master_index` columns (`cik`, `company_name`, `form_type`, `date_filed`, `filename`) for context.
- Handle `NULL` `submissions` data for non-XBRL filers.

#### c. Filing History & Trends
**Examples**:
1. **How many 10-K filings submitted by financial firms in Q1 2025?**
   ```sql
   SELECT COUNT(*) AS filing_count
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type = '10-K'
     AND m.date_filed BETWEEN '2025-01-01' AND '2025-03-31'
     AND (s.sic LIKE '60%' OR s.sic IS NULL);
   ```
   - **Logic**: Drive with `master_index` for 10-K; filter financial SIC codes.

2. **List all companies that changed their registration status in the past year**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.afs, s.filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.date_filed >= '2024-06-28'
     AND s.afs IS NOT NULL
   ORDER BY m.company_name, s.filed;
   ```
   - **Logic**: Use `master_index` for date filter; compare `s.afs` for changes.

3. **Which companies filed both 10-K and 8-K in the last 30 days?**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type IN ('10-K', '8-K')
     AND m.date_filed >= date('2025-06-28', '-30 days')
   GROUP BY m.cik, s.name
   HAVING COUNT(DISTINCT m.form_type) = 2;
   ```
   - **Logic**: Drive with `master_index`; use `GROUP BY` for both form types.

**LLM Guidance**:
- Use `master_index` as driving table for filing history.
- Apply filters on `m.form_type` and `m.date_filed` first.
- Include `submissions` data via `LEFT JOIN` for additional context.

#### d. Audit & Compliance Checks
**Examples**:
1. **Highlight discrepancies between Bloomberg 13F and EDGAR-derived registration status**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.afs
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type IN ('13F-HR', '13F-NT')
     AND (s.afs NOT IN ('LAF', 'ACC', 'SRA') OR s.afs IS NULL)
     AND m.date_filed <= '2025-06-30';
   ```
   - **Logic**: Drive with `master_index` for 13F forms; check `s.afs` for discrepancies.

2. **Generate report of all companies missing registration status**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE s.afs IS NULL
   ORDER BY m.company_name;
   ```
   - **Logic**: Use `master_index` to include all companies; filter for `NULL` `s.afs`.

3. **Which companies have not filed a 10-K in the past 12 months?**
   ```sql
   SELECT DISTINCT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type != '10-K'
     OR m.date_filed < '2024-06-28'
   ORDER BY m.company_name;
   ```
   - **Logic**: Drive with `master_index`; exclude recent 10-K filings.

**LLM Guidance**:
- Start with `master_index` for audit queries.
- Use `LEFT JOIN` to handle missing `submissions` data.
- Include all `master_index` columns for context.

#### e. Advanced Filtering & Export
**Examples**:
1. **Export all Section 12 registered companies in the healthcare sector**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.afs, s.sic, s.countryba, s.stprba, s.cityba
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE s.afs IN ('LAF', 'ACC', 'SRA')
     AND (s.sic BETWEEN 8000 AND 8099 OR s.sic IS NULL)
   ORDER BY m.company_name;
   ```
   - **Logic**: Drive with `master_index`; filter Section 12 and healthcare SIC.

2. **Show all filings with executive changes and export metadata to JSON**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE m.form_type = '8-K'
     AND m.date_filed <= '2025-06-30'
   ORDER BY m.date_filed DESC;
   ```
   - **Logic**: Use `master_index` for 8-K filings; include metadata for export.

3. **List all companies with SIC code starting with 60 and registered under Section 12**
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.afs, s.sic
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE s.afs IN ('LAF', 'ACC', 'SRA')
     AND (s.sic LIKE '60%' OR s.sic IS NULL)
   ORDER BY m.company_name;
   ```
   - **Logic**: Drive with `master_index`; filter financial SIC and Section 12.

**LLM Guidance**:
- Use `master_index` as driving table for filtering/export.
- Include comprehensive columns from `master_index` and `submissions`.
- Structure results for JSON with clear columns.

### 4. Error Handling
- **Invalid CIK**: Strip leading zeros; validate format.
- **Unknown Form Type**: Suggest valid form types (e.g., `10-K`, `13F-HR`).
- **Date Mismatch**: Use `master_index.date_filed` primarily; normalize `submissions.filed` (YYYYMMDD) to YYYY-MM-DD.
- **No Results**: Return “No matching records found” with context (e.g., “No filings for Apple in 2025”).
- **Missing Data**: Handle `NULL` values in `submissions` (e.g., `s.sic IS NULL`) for non-XBRL filers.

### 5. Performance Optimization
- Filter on `master_index` columns (e.g., `cik`, `form_type`, `date_filed`) first to reduce scans.
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
**User Input**: “What is the SIC code for Apple?”
**Steps**:
1. Identify entities:
   - Company: Apple (`m.company_name LIKE '%APPLE%'`, CIK: `320193`)
   - Data: SIC code (`s.sic`)
2. Construct query:
   ```sql
   SELECT m.cik, m.company_name, m.form_type, m.date_filed, s.sic, s.countryba, s.stprba, s.cityba
   FROM master_index m
   LEFT JOIN submissions s ON s.cik = m.cik
   WHERE UPPER(m.company_name) LIKE '%APPLE%'
   ORDER BY m.date_filed DESC
   LIMIT 10;
   ```
3. Validate:
   - Confirm name pattern and CIK (if known).
   - Ensure `master_index` is driving table.
   - Handle `NULL` `s.sic` for non-XBRL filings.

## Notes for LLM
- **Context Awareness**: Use conversation history to refine queries (e.g., reuse CIK from prior input).
- **Flexibility**: Support variations (e.g., “Apple Inc.”, “Apple”, CIK `320193`).
- **Comprehensive Data**: Always include key columns from `master_index` (`cik`, `company_name`, `form_type`, `date_filed`, `filename`) and relevant `submissions` columns for metadata queries.
- **Driving Table**: Always start queries with `FROM master_index m` to ensure all filings are considered.
- **Export Handling**: For JSON exports, suggest fields like `m.cik`, `m.company_name`, `m.form_type`, `s.name`, `s.sic`.
- **Limitations**:
  - `submissions` and `presentation_of_statement` only include XBRL filings; rely on `master_index` for complete coverage.
  - Executive team data requires parsing filing documents (not in database).
  - Registration status changes need external comparison logic.
  - Bloomberg 13F data is external; compare only with EDGAR `form_type` and `afs`.
- **Memory Management**: If users request to forget chats, instruct them to:
  - Click the book icon under the message and select the chat to forget.
  - Disable memory in the “Data Controls” section of settings.

## Security Reminder
- Restrict to `SELECT` queries only.
- Sanitize inputs to prevent SQL injection (e.g., escape special characters).