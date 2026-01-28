from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import dotenv_values


engine = create_engine(
    dotenv_values(".env")["DATABASE_URL"]
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()