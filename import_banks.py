import csv
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Account, Transaction, Bank, Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Your DB config (update as needed)
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank"  # Your actual DB name

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def import_customers(csv_path):
    if not os.path.exists(csv_path):
        logging.error(f"Customer CSV file does not exist: {csv_path}")
        return

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                customers_added = 0
                accounts_added = 0
                for row in reader:
                    # CSV columns: Customer, Address, Phone, Personnummer, BankAccount
                    customer_name = row.get("Customer")
                    address = row.get("Address")
                    phone = row.get("Phone")
                    personnummer = row.get("Personnummer")
                    account_number = row.get("BankAccount")

                    if not customer_name or not account_number:
                        logging.warning("Skipping row with missing customer name or account number")
                        continue

                    # Check if customer exists
                    customer = session.query(Customer).filter_by(personnummer=personnummer).first()
                    if not customer:
                        customer = Customer(
                            customer_name=customer_name,
                            address=address,
                            phone=phone,
                            personnummer=personnummer
                        )
                        session.add(customer)
                        session.flush()  # to get customer_id

                        customers_added += 1

                    # Check if account exists
                    account = session.query(Account).filter_by(account_number=account_number).first()
                    if not account:
                        account = Account(
                            account_number=account_number,
                            customer_id=customer.customer_id,
                            country=None,
                            municipality=None
                        )
                        session.add(account)
                        accounts_added += 1

                session.commit()
                logging.info(f"Imported {customers_added} customers and {accounts_added} accounts from {csv_path}")

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Database error during customer import: {e}")
        except Exception as e:
            logging.error(f"Error reading customer CSV or processing data: {e}")

def import_transactions(csv_path):
    if not os.path.exists(csv_path):
        logging.error(f"Transaction CSV file does not exist: {csv_path}")
        return

    with SessionLocal() as session:
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                transactions_added = 0
                for row in reader:
                    # CSV columns: transaction_id, timestamp, amount, currency, sender_account, receiver_account, sender_country, sender_municipality, receiver_country, receiver_municipality, transaction_type, notes
                    transaction_id = row.get("transaction_id")
                    timestamp = row.get("timestamp")
                    amount = float(row.get("amount") or 0)
                    currency = row.get("currency")
                    sender_account = row.get("sender_account")
                    receiver_account = row.get("receiver_account")
                    sender_country = row.get("sender_country")
                    sender_municipality = row.get("sender_municipality")
                    receiver_country = row.get("receiver_country")
                    receiver_municipality = row.get("receiver_municipality")
                    transaction_type = row.get("transaction_type")
                    notes = row.get("notes")

                    if not transaction_id or not sender_account or not receiver_account:
                        logging.warning("Skipping incomplete transaction row")
                        continue

                    # Check if transaction already exists by transaction_id
                    existing_tx = session.query(Transaction).filter_by(transaction_id=transaction_id).first()
                    if existing_tx:
                        logging.info(f"Transaction {transaction_id} already exists. Skipping.")
                        continue

                    transaction = Transaction(
                        transaction_id=transaction_id,
                        timestamp=timestamp,
                        amount=amount,
                        currency=currency,
                        sender_account=sender_account,
                        receiver_account=receiver_account,
                        sender_country=sender_country,
                        sender_municipality=sender_municipality,
                        receiver_country=receiver_country,
                        receiver_municipality=receiver_municipality,
                        transaction_type=transaction_type,
                        notes=notes
                    )
                    session.add(transaction)
                    transactions_added += 1

                session.commit()
                logging.info(f"Imported {transactions_added} transactions from {csv_path}")

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Database error during transaction import: {e}")
        except Exception as e:
            logging.error(f"Error reading transaction CSV or processing data: {e}")

if __name__ == "__main__":
    customer_csv_path = r".\data\sebank_customers_with_accounts.csv"   # put your actual path here
    transaction_csv_path = r".\data\transactions.csv"
    import_customers(customer_csv_path)
    import_transactions(transaction_csv_path)
