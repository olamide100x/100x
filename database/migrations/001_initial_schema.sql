CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50),
  contact_email VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  asset_type VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  external_id VARCHAR(100),
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  status VARCHAR(50),
  operator_name VARCHAR(255),
  field_name VARCHAR(255),
  county VARCHAR(100),
  state VARCHAR(2) DEFAULT 'TX',
  age_years INTEGER,
  first_production_date DATE,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source VARCHAR(50) NOT NULL,
  external_id VARCHAR(100),
  incident_type VARCHAR(100),
  incident_date DATE NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  operator_name VARCHAR(255),
  description TEXT,
  severity VARCHAR(50),
  injuries INTEGER DEFAULT 0,
  fatalities INTEGER DEFAULT 0,
  property_damage DECIMAL(15, 2),
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE weather_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type VARCHAR(100),
  event_date DATE NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  severity VARCHAR(50),
  description TEXT,
  affected_radius_km DECIMAL(10, 2),
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE risk_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
  score DECIMAL(5, 2) NOT NULL,
  score_category VARCHAR(50),
  calculation_date TIMESTAMP DEFAULT NOW(),
  factors JSONB NOT NULL,
  version INTEGER DEFAULT 1,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE risk_factors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  risk_score_id UUID REFERENCES risk_scores(id) ON DELETE CASCADE,
  factor_type VARCHAR(100) NOT NULL,
  factor_name VARCHAR(255) NOT NULL,
  impact_score DECIMAL(5, 2) NOT NULL,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  report_type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  generated_by UUID,
  asset_ids UUID[],
  report_date DATE NOT NULL,
  file_url TEXT,
  file_size_bytes INTEGER,
  status VARCHAR(50) DEFAULT 'pending',
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE data_sync_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source VARCHAR(50) NOT NULL,
  job_type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL,
  records_processed INTEGER DEFAULT 0,
  records_added INTEGER DEFAULT 0,
  records_updated INTEGER DEFAULT 0,
  error_message TEXT,
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  metadata JSONB
);
