import csv
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Customer

DATABASE_URL = 'postgresql+psycopg2://postgres:admin@localhost:5432/bank'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_personnummer(pnr: str) -> str:
    return pnr.replace("-", "").strip()

def import_customers(csv_file):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            added = 0
            updated = 0

            for row in reader:
                raw_pnr = row.get('Personnummer', '').strip()
                personnummer = normalize_personnummer(raw_pnr)

                if not personnummer:
                    logger.warning(f"Skipping row without personnummer: {row}")
                    continue

                customer_name = row.get('Name', '').strip()
                address = row.get('Address', '').strip()
                phone = row.get('Phone', '').strip()
                email = row.get('Email', '').strip()

                # Check if customer exists by normalized personnummer
                existing_customer = session.query(Customer).filter(
                    func.replace(func.trim(Customer.personnummer), '-', '') == personnummer
                ).first()

                if existing_customer:
                    # Optionally update fields if you want
                    # For example:
                    # existing_customer.customer_name = customer_name or existing_customer.customer_name
                    # existing_customer.address = address or existing_customer.address
                    # existing_customer.phone = phone or existing_customer.phone
                    # existing_customer.email = email or existing_customer.email
                    updated += 1
                    logger.info(f"Customer {personnummer} already exists. Skipping insert.")
                else:
                    new_customer = Customer(
                        customer_name=customer_name,
                        personnummer=raw_pnr,  # keep original format with dash
                        address=address,
                        phone=phone,
                        email=email
                    )
                    session.add(new_customer)
                    added += 1

            session.commit()
            logger.info(f"Import complete: {added} added, {updated} existed.")

    except Exception as e:
        logger.error(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    csv_path = r'.\data\sebank_customers_with_accounts.csv'

    import_customers(csv_path)
