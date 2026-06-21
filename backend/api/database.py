"""
Database configuration and models for TibbWell
Supports both PostgreSQL (production) and SQLite (local development)
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database URL from environment variable, with SQLite fallback for local dev
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./tibbwell.db"
)

# Create engine
# For PostgreSQL, use psycopg2; for SQLite, use sqlite-specific connect args
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # SQLite specific
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session - use with FastAPI Depends()"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
