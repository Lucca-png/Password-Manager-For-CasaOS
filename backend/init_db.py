#!/usr/bin/env python3
"""Initialize the database"""
import os
import sys

# Set up path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set database URL to use relative path
os.environ['DATABASE_URL'] = 'sqlite:///./data/vault.db'

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Create engine with proper path
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vault.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

print(f"Database path: {db_path}")
print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Import models
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)
print("✅ Database initialized successfully!")
print(f"Database file: {db_path}")
