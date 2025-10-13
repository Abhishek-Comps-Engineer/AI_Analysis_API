from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"Database connected: {settings.database_name}", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)


Base = declarative_base()

def  get_db():
   db = SessionLocal()
   try:
      yield db 
   finally:
      db.close()
