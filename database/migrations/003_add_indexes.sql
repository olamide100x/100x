CREATE INDEX IF NOT EXISTS idx_assets_org ON assets(organization_id);
CREATE INDEX IF NOT EXISTS idx_assets_location ON assets USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_assets_external_id ON assets(external_id);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status);

CREATE INDEX IF NOT EXISTS idx_incidents_date ON incidents(incident_date);
CREATE INDEX IF NOT EXISTS idx_incidents_location ON incidents USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_incidents_operator ON incidents(operator_name);
CREATE INDEX IF NOT EXISTS idx_incidents_source ON incidents(source);
CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);

CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_events(event_date);
CREATE INDEX IF NOT EXISTS idx_weather_location ON weather_events USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_weather_type ON weather_events(event_type);

CREATE INDEX IF NOT EXISTS idx_risk_scores_asset ON risk_scores(asset_id);
CREATE INDEX IF NOT EXISTS idx_risk_scores_date ON risk_scores(calculation_date);
CREATE INDEX IF NOT EXISTS idx_risk_scores_score ON risk_scores(score);
CREATE INDEX IF NOT EXISTS idx_risk_scores_category ON risk_scores(score_category);

CREATE INDEX IF NOT EXISTS idx_risk_factors_score ON risk_factors(risk_score_id);
CREATE INDEX IF NOT EXISTS idx_risk_factors_type ON risk_factors(factor_type);

CREATE INDEX IF NOT EXISTS idx_reports_org ON reports(organization_id);
CREATE INDEX IF NOT EXISTS idx_reports_date ON reports(report_date);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);

CREATE INDEX IF NOT EXISTS idx_sync_jobs_source ON data_sync_jobs(source);
CREATE INDEX IF NOT EXISTS idx_sync_jobs_status ON data_sync_jobs(status);
CREATE INDEX IF NOT EXISTS idx_sync_jobs_started ON data_sync_jobs(started_at);
