import csv
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Customer, Account

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Database settings
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bank'

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# CSV file path
CSV_PATH = r'./data/sebank_customers_with_accounts.csv'

def parse_address_for_location(address):
    """Try to extract country and municipality from address. Simplified logic."""
    if ',' in address:
        parts = address.split(',')
        municipality = parts[-1].strip()
        country = 'Sweden'  # Hardcoded for SE bank data
    else:
        municipality = None
        country = None
    return country, municipality

def import_missing_accounts(csv_path):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Base.metadata.create_all(engine)

        existing_accounts = set(acc.account_number for acc in session.query(Account.account_number).all())
        logger.info(f"Found {len(existing_accounts)} existing accounts in DB.")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            logger.info(f"CSV headers found: {reader.fieldnames}")

            new_accounts = 0
            for row in reader:
                account_number = row.get('BankAccount')
                if not account_number:
                    logger.warning(f"⚠️ Skipping row with missing BankAccount: {row}")
                    continue

                if account_number in existing_accounts:
                    logger.warning(f"⚠️ Account {account_number} already exists. Skipping.")
                    continue

                personnummer = row.get('Personnummer')
                customer = session.query(Customer).filter_by(personnummer=personnummer).first()

                if not customer:
                    # Create new customer
                    customer = Customer(
                        customer_name=row.get('Customer'),
                        address=row.get('Address'),
                        phone=row.get('Phone'),
                        personnummer=personnummer,
                        email=None  # No email in CSV
                    )
                    session.add(customer)
                    session.flush()  # Assigns customer_id

                # Extract location info
                address = row.get('Address', '')
                country, municipality = parse_address_for_location(address)

                account = Account(
                    account_number=account_number,
                    customer_id=customer.customer_id,
                    bank_id=None,  # No bank info in CSV
                    country=country,
                    municipality=municipality
                )
                session.add(account)
                existing_accounts.add(account_number)
                new_accounts += 1

            session.commit()
            logger.info(f"✅ Import completed. {new_accounts} new accounts added.")

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"❌ Database error, rolled back changes: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"❌ General error, rolled back changes: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    import_missing_accounts(CSV_PATH)
