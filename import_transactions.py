import csv
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    amount = Column(Float)
    currency = Column(String)
    sender_account = Column(String, ForeignKey('accounts.account_number'), nullable=False)
    receiver_account = Column(String, ForeignKey('accounts.account_number'), nullable=False)
    sender_country = Column(String, nullable=True)
    sender_municipality = Column(String, nullable=True)
    receiver_country = Column(String, nullable=True)
    receiver_municipality = Column(String, nullable=True)
    transaction_type = Column(String, nullable=True)
    notes = Column(String, nullable=True)

# Database URL
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"

# Create engine and session factory
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

def import_transactions(csv_file_path):
    session = Session()
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transaction = Transaction(
                    timestamp=parse_datetime(row.get('timestamp')),
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
            session.commit()
        print("Transactions imported successfully!")
    except (SQLAlchemyError, IOError) as e:
        session.rollback()
        print(f"Error occurred during import, rolled back. Details: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    csv_path = r".\data\transactions.csv"
    import_transactions(csv_path)
