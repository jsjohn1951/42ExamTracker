from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db";
user = os.getenv("POSTGRES_USER");
password = os.getenv("POSTGRES_PASSWORD");
database = os.getenv("POSTGRES_DB");
port = os.getenv("POSTGRES_PORT");

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@db:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL);

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);

Base = declarative_base();