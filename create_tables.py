import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Base

from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"

def main():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    main()
