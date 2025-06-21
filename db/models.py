import os
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use connection pooling for better cloud compatibility
DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///c:/Users/rites/vsCodePractice/db/agents.db')

# Import cloud-optimized engine creation
try:
    from .connection import create_cloud_engine
    engine = create_cloud_engine(DB_URL)
except ImportError:
    # Fallback to simple engine creation if connection utility is not available
    from sqlalchemy import create_engine
    
    if DB_URL and 'supabase.co' in DB_URL:
        engine = create_engine(
            DB_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={"sslmode": "require"}
        )
    else:
        engine = create_engine(
            DB_URL, 
            connect_args={"check_same_thread": False} if DB_URL.startswith('sqlite') else {}
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    source = Column(String)
    type = Column(String)
    tags = Column(String)
    deployment = Column(String)
    license = Column(String)
    repo_link = Column(String)
    demo_link = Column(String)
    paper_link = Column(String)
    last_updated = Column(String)
    related = Column(String)
    rating = Column(String)
    install = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_all_agents():
    db = SessionLocal()
    agents = db.query(Agent).all()
    db.close()
    return [a.__dict__ for a in agents]

def search_agents(q: str):
    db = SessionLocal()
    agents = db.query(Agent).filter(
        (Agent.name.ilike(f'%{q}%')) |
        (Agent.description.ilike(f'%{q}%'))
    ).all()
    db.close()
    return [a.__dict__ for a in agents]
