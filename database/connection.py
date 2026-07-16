from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def get_engine():
    """
    Return the SQLAlchemy engine.
    """
    return engine


def test_connection():
    """
    Test the PostgreSQL connection.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("=" * 60)
        print(" RetailIQ AI - PostgreSQL Connection")
        print("=" * 60)
        print(f"Database : {DB_NAME}")
        print(f"User     : {DB_USER}")
        print(f"Host     : {DB_HOST}")
        print(f"Port     : {DB_PORT}")
        print("Status   : Connected Successfully ✅")
        print("=" * 60)

    except Exception as e:
        print("=" * 60)
        print(" Connection Failed ❌")
        print("=" * 60)
        print(e)


if __name__ == "__main__":
    test_connection()