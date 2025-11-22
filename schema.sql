-- Create schema
CREATE SCHEMA IF NOT EXISTS hygen_re;

-- Set search path
SET search_path TO hygen_re;

-- Create builders table
CREATE TABLE IF NOT EXISTS hygen_re.builders (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),
    contact_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create projects table
CREATE TABLE IF NOT EXISTS hygen_re.projects (
    id SERIAL PRIMARY KEY,
    builder_id INTEGER NOT NULL REFERENCES hygen_re.builders(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    project_type VARCHAR(50),
    location VARCHAR(255),
    price_range VARCHAR(100),
    bhk_options VARCHAR(255),
    possession_date VARCHAR(100),
    amenities JSONB DEFAULT '[]'::jsonb,
    wa_entry_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create leads table
CREATE TABLE IF NOT EXISTS hygen_re.leads (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES hygen_re.projects(id) ON DELETE CASCADE,
    wa_phone VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    budget_min BIGINT,
    budget_max BIGINT,
    bhk_preference VARCHAR(50),
    location_pref VARCHAR(255),
    current_state VARCHAR(100) DEFAULT 'NEW',
    status VARCHAR(100) DEFAULT 'NEW',
    visit_interested BOOLEAN DEFAULT FALSE,
    visit_date DATE,
    visit_slot VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, wa_phone)
);

-- Create conversations table
CREATE TABLE IF NOT EXISTS hygen_re.conversations (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER NOT NULL REFERENCES hygen_re.leads(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create messages table
CREATE TABLE IF NOT EXISTS hygen_re.messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES hygen_re.conversations(id) ON DELETE CASCADE,
    sender VARCHAR(50) NOT NULL,
    message_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leads_project_id ON hygen_re.leads(project_id);
CREATE INDEX IF NOT EXISTS idx_leads_wa_phone ON hygen_re.leads(wa_phone);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON hygen_re.messages(conversation_id);

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON SCHEMA hygen_re TO hygen_re_db_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA hygen_re TO hygen_re_db_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA hygen_re TO hygen_re_db_user;
