#!/usr/bin/env python
"""
Database migration script to create schema and tables
Run this once after deploying to Render
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings

def create_schema():
    """Create database schema and tables"""
    engine = create_engine(settings.DATABASE_URL)
    
    sql_commands = [
        # Create schema
        "CREATE SCHEMA IF NOT EXISTS hygen_re;",
        
        # Create builders table
        """
        CREATE TABLE IF NOT EXISTS hygen_re.builders (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            contact_name VARCHAR(255),
            contact_phone VARCHAR(50),
            contact_email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Create projects table
        """
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
        """,
        
        # Create leads table
        """
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
        """,
        
        # Create conversations table
        """
        CREATE TABLE IF NOT EXISTS hygen_re.conversations (
            id SERIAL PRIMARY KEY,
            lead_id INTEGER NOT NULL REFERENCES hygen_re.leads(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Create messages table
        """
        CREATE TABLE IF NOT EXISTS hygen_re.messages (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER NOT NULL REFERENCES hygen_re.conversations(id) ON DELETE CASCADE,
            sender VARCHAR(50) NOT NULL,
            message_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Create indexes
        "CREATE INDEX IF NOT EXISTS idx_leads_project_id ON hygen_re.leads(project_id);",
        "CREATE INDEX IF NOT EXISTS idx_leads_wa_phone ON hygen_re.leads(wa_phone);",
        "CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON hygen_re.messages(conversation_id);",
    ]
    
    print("🔄 Creating database schema...")
    
    with engine.connect() as conn:
        for i, sql in enumerate(sql_commands, 1):
            try:
                conn.execute(text(sql))
                conn.commit()
                print(f"✅ Step {i}/{len(sql_commands)}: Success")
            except Exception as e:
                print(f"⚠️  Step {i}/{len(sql_commands)}: {str(e)}")
    
    print("\n✅ Database schema creation complete!")
    print("\nVerifying tables...")
    
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'hygen_re' ORDER BY tablename")
        )
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("❌ No tables found!")

if __name__ == "__main__":
    create_schema()
