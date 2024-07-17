import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




#!Important
from dotenv import load_dotenv


#load enviroment variables from.env file

load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine =create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal =sessionmaker(autocommit=False, autoflush=False,bind=engine)
