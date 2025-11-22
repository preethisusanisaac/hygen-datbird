# app/models/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.database_url_with_driver, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_db():
    from sqlalchemy.orm import Session
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database schema and tables"""
    from sqlalchemy import text
    import time
    
    # Retry logic for database connection (useful for Render cold starts)
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Create schema first
            with engine.connect() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS hygen_re"))
                conn.commit()
            
            # Import models in correct order (parent tables before child tables with foreign keys)
            # This ensures tables are registered with Base in dependency order
            from app.models import builder  # noqa: F401
            from app.models import project  # noqa: F401 (depends on builder)
            from app.models import lead  # noqa: F401 (depends on project)
            
            # Create all tables - SQLAlchemy will respect the order of dependencies
            Base.metadata.create_all(bind=engine)
            
            print("✅ Database initialized successfully")
            break
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Database connection attempt {attempt + 1} failed: {e}")
                print(f"   Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"❌ Failed to initialize database after {max_retries} attempts: {e}")
                raise
