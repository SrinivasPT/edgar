-- cSpell:disable

-- Create the master index table to store basic company information
CREATE TABLE IF NOT EXISTS master_index (
    cik INTEGER, 
    company_name TEXT, 
    form_type TEXT, 
    date_filed TEXT, 
    filename TEXT
);

-- Submissions table based on EDGAR SUB data set specification
CREATE TABLE IF NOT EXISTS submissions (
    -- Primary key and core identifiers
    adsh TEXT(20) NOT NULL PRIMARY KEY,  -- Accession Number (format: nnnnnnnnnn-nn-nnnnnn)
    cik INTEGER NOT NULL,                -- Central Index Key (10 digit number)
    name TEXT(150) NOT NULL,             -- Name of registrant
    
    -- Business classification
    sic INTEGER,                         -- Standard Industrial Classification (4 digit)
    
    -- Business address fields
    countryba TEXT(2),                   -- ISO 3166-1 country code for business address
    stprba TEXT(2),                      -- State/province for business address
    cityba TEXT(30),                     -- City for business address
    zipba TEXT(10),                      -- Zip code for business address
    bas1 TEXT(40),                       -- Business address line 1
    bas2 TEXT(40),                       -- Business address line 2
    baph TEXT(20),                       -- Business address phone number
    
    -- Mailing address fields
    countryma TEXT(2),                   -- ISO 3166-1 country code for mailing address
    stprma TEXT(2),                      -- State/province for mailing address
    cityma TEXT(30),                     -- City for mailing address
    zipma TEXT(10),                      -- Zip code for mailing address
    mas1 TEXT(40),                       -- Mailing address line 1
    mas2 TEXT(40),                       -- Mailing address line 2
    
    -- Incorporation details
    countryinc TEXT(3),                  -- ISO 3166-1 country of incorporation
    stprinc TEXT(2),                     -- State/province of incorporation
    ein INTEGER,                         -- Employee Identification Number (9 digit)
    
    -- Name change history
    former TEXT(150),                    -- Most recent former name
    changed TEXT(8),                     -- Date of name change (YYYYMMDD format)
    
    -- SEC filing status and characteristics
    afs TEXT(5),                         -- Filer status (LAF, ACC, SRA, NON, SML)
    wksi INTEGER NOT NULL,               -- Well Known Seasoned Issuer (0 or 1)
    fye TEXT(4),                         -- Fiscal Year End (MMDD format)
    
    -- Filing details
    form TEXT(10) NOT NULL,              -- Submission type
    period TEXT(8) NOT NULL,             -- Balance Sheet Date (YYYYMMDD)
    fy INTEGER,                          -- Fiscal Year (YYYY)
    fp TEXT(2),                          -- Fiscal Period (FY, Q1, Q2, Q3, Q4)
    filed TEXT(8) NOT NULL,              -- Filing date (YYYYMMDD)
    accepted TEXT(19) NOT NULL,          -- Acceptance datetime (YYYY-MM-DD HH:MM:SS)
    
    -- Submission characteristics
    prevrpt INTEGER NOT NULL,            -- Previous Report flag (0 or 1)
    detail INTEGER NOT NULL,             -- Detail level flag (0 or 1)
    instance TEXT(40) NOT NULL,          -- XBRL Instance Document name
    
    -- Co-registrant information
    nciks INTEGER NOT NULL,              -- Number of CIKs included
    aciks TEXT(120)                      -- Additional CIKs (space delimited)
);

-- Presentation of Statements table based on EDGAR PRE data set specification
CREATE TABLE IF NOT EXISTS presentation_of_statement (
    -- Composite primary key fields
    adsh TEXT(20) NOT NULL,              -- Accession Number (format: nnnnnnnnnn-nn-nnnnnn)
    report INTEGER NOT NULL,             -- Report grouping (R file number)
    line INTEGER NOT NULL,               -- Presentation line order within report
    
    -- Statement classification
    stmt TEXT(2) NOT NULL,               -- Financial statement type (BS, IS, CF, EQ, CI, SI, UN)
    
    -- Presentation characteristics
    inpth INTEGER NOT NULL,              -- Parenthetical presentation flag (0 or 1)
    rfile TEXT(1) NOT NULL,              -- Interactive data file type (H = .htm, X = .xml)
    
    -- Tag information
    tag TEXT(256) NOT NULL,              -- Filer-chosen tag for line item
    version TEXT(20) NOT NULL,           -- Taxonomy identifier or adsh
    
    -- Display information
    plabel TEXT(512) NOT NULL,           -- Preferred label text for line item
    negating INTEGER NOT NULL,           -- Negating label flag (0 or 1)
    
    -- Define composite primary key
    PRIMARY KEY (adsh, report, line),
    
    -- Foreign key constraint to submissions table
    FOREIGN KEY (adsh) REFERENCES submissions(adsh)
);
