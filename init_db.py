#!/usr/bin/env python3
"""
Database initialization script for AI Agent Discovery project.
Sets up PostgreSQL database with proper tables and indexes.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the db directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'db')))
from models import Base, Agent, init_db

def validate_environment():
    """Validate required environment variables."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ ERROR: DATABASE_URL environment variable is required")
        print("Example: export DATABASE_URL='postgresql://user:password@localhost:5432/dbname'")
        sys.exit(1)
    
    if db_url.startswith('sqlite'):
        print("⚠️  WARNING: Using SQLite. For production, use PostgreSQL.")
    
    return db_url

def create_indexes(engine):
    """Create database indexes for better performance."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name);",
        "CREATE INDEX IF NOT EXISTS idx_agents_source ON agents(source);",
        "CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(type);",
        "CREATE INDEX IF NOT EXISTS idx_agents_tags ON agents USING gin(to_tsvector('english', tags));",
        "CREATE INDEX IF NOT EXISTS idx_agents_description ON agents USING gin(to_tsvector('english', description));"
    ]
    
    with engine.connect() as conn:
        for index_sql in indexes:
            try:
                conn.execute(text(index_sql))
                print(f"✅ Created index: {index_sql.split('idx_')[1].split(' ')[0]}")
            except SQLAlchemyError as e:
                if "already exists" not in str(e):
                    print(f"⚠️  Index creation warning: {e}")

def main():
    """Initialize the database with tables and indexes."""
    print("🚀 AI Agent Discovery - Database Initialization")
    print("=" * 50)
    
    # Validate environment
    db_url = validate_environment()
    print(f"📊 Database URL: {db_url.split('@')[0]}@***")
    
    try:
        # Create engine and test connection
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print("✅ Database connection successful")
        
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        
        # Create indexes for performance
        print("🔍 Creating database indexes...")
        create_indexes(engine)
        
        # Test Agent model
        print("🧪 Testing Agent model...")
        from models import SessionLocal
        db = SessionLocal()
        count = db.query(Agent).count()
        db.close()
        print(f"✅ Agent table ready. Current records: {count}")
        
        print("\n🎉 Database initialization complete!")
        print("💡 Next steps:")
        print("   1. Run ingestion scripts: python -m ingest.arxiv_ingest")
        print("   2. Start API server: uvicorn main:app --reload")
        print("   3. Start frontend: cd web && npm start")
        
    except SQLAlchemyError as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
