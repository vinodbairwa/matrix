from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import OperationalError

Base = declarative_base()  # This is your declarative base

# Add database connection URL here
DATABASE_URL = 'mysql+pymysql://root:vinod@localhost/matrix'


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError:
        db.rollback()
    finally:
        db. close()

