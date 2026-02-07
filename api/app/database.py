import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")


def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            return engine
        except OperationalError:
            print("⏳ Waiting for database...")
            time.sleep(2)


engine = wait_for_db()

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
