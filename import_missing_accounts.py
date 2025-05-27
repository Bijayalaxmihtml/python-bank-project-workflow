import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Account, Base  # make sure this points to your models.py

# Database connection settings
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bank'  # your database name

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# CSV file path
CSV_PATH = r'./data/sebank_customers_with_accounts.csv'

def import_accounts(csv_path):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables if not already there
    Base.metadata.create_all(engine)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                account = Account(
                    account_number=row['account_number'],
                    customer_id=int(row['customer_id']),
                    bank_id=int(row['bank_id']) if row['bank_id'] else None,
                    country=row.get('country'),
                    municipality=row.get('municipality')
                )
                session.add(account)
            except Exception as e:
                print(f"Skipping row due to error: {e}")
        session.commit()
    print("Accounts imported successfully.")

if __name__ == "__main__":
    import_accounts(CSV_PATH)
