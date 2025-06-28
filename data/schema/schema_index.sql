-- Create indexes on master_index table for better query performance
CREATE INDEX IF NOT EXISTS idx_master_index_cik ON master_index(cik);
CREATE INDEX IF NOT EXISTS idx_master_index_company_name ON master_index(company_name);
CREATE INDEX IF NOT EXISTS idx_master_index_form_type ON master_index(form_type);

-- Create indexes for common query patterns
CREATE INDEX idx_presentation_adsh ON presentation_of_statement(adsh);
CREATE INDEX idx_presentation_stmt ON presentation_of_statement(stmt);
CREATE INDEX idx_presentation_tag ON presentation_of_statement(tag);
CREATE INDEX idx_presentation_report_line ON presentation_of_statement(report, line);

-- Create indexes for common query patterns
CREATE INDEX idx_submissions_cik ON submissions(cik);
CREATE INDEX idx_submissions_filed ON submissions(filed);
CREATE INDEX idx_submissions_form ON submissions(form);
CREATE INDEX idx_submissions_period ON submissions(period);
CREATE INDEX idx_submissions_fy_fp ON submissions(fy, fp);


