import csv
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from models import Base, Transaction  # Import your models here

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def parse_datetime(dt_str: str) -> Optional[datetime]:
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

def import_transactions(csv_file_path: str) -> None:
    session = Session()
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    transaction = Transaction(
                        timestamp=parse_datetime(row.get('timestamp', '')),
                        amount=float(row.get('amount', 0)),
                        currency=row.get('currency'),
                        sender_account=row.get('sender_account'),
                        receiver_account=row.get('receiver_account'),
                        sender_country=row.get('sender_country'),
                        sender_municipality=row.get('sender_municipality'),
                        receiver_country=row.get('receiver_country'),
                        receiver_municipality=row.get('receiver_municipality'),
                        transaction_type=row.get('transaction_type'),
                        notes=row.get('notes')
                    )
                    session.add(transaction)
                except Exception as row_err:
                    logger.error(f"Skipping row due to error: {row_err}, data: {row}")
            session.commit()
        logger.info("Transactions imported successfully!")
    except (SQLAlchemyError, IOError) as e:
        session.rollback()
        logger.error(f"Error occurred during import, rolled back. Details: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Create tables if they don't exist (only run once)
    Base.metadata.create_all(engine)

    csv_path = r".\data\transactions.csv"
    import_transactions(csv_path)


