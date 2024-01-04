from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = Config()

# 1. 資料庫
engine = create_engine(Config.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
