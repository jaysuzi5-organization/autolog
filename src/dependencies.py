from time import sleep
from sqlalchemy import text
from framework.db import Database
from models.base import Base

max_retries = 5
retry_delay = 2
database = None

def setup_db(logger):
    global database
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})")
            database = Database(Base)
            session = database.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            logger.info("Database connection established successfully")
            break
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error("Max retries reached, failing startup")
                raise
            sleep(retry_delay)


def get_db():
    session = None
    if database:
        session = database.get_session()
    try:
        yield session
    finally:
        if session:
            session.close()
