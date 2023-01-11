from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from core.config import settings
import pandas as pd

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def populate_db():
    data_from_google_drive = pd.read_csv('sample-products.csv')
    data_from_google_drive.to_sql('products', engine, if_exists='append')
    return "Done"



def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
        print("Scuccess")
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)