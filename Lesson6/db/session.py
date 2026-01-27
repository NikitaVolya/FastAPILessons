from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import dotenv_values


engine = create_engine(
    dotenv_values(".env")["DATABASE_URL"],
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Session:
    dp = SessionLocal()
    try:
        yield dp
    finally:
        dp.close()