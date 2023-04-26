from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

def initialize_database():
    load_dotenv()
    engine = create_engine(os.getenv("DB_URL"), echo=True)
    global SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(engine)
        
def get_local_session():
    return SessionLocal()