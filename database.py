from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite for development, use PostgreSQL if available
postgresql_url = os.getenv('POSTGRESQL_DATABASE_URL')
if postgresql_url:
    # Handle URL encoding for database names with spaces
    SQLALCHEMY_DATABASE_URL = postgresql_url.replace('%20', ' ')
else:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///./Messages.db'

# Create engine with appropriate connection args
if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
