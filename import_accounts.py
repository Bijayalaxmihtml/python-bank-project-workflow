import csv
import logging
from sqlalchemy import create_engine, func, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# === Models ===

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    personnummer = Column(String, unique=True)
    email = Column(String)

    accounts = relationship('Account', back_populates='customer')


class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    swift_code = Column(String, unique=True)

    accounts = relationship('Account', back_populates='bank')


class Account(Base):
    __tablename__ = 'accounts'

    account_number = Column(String, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=True)
    country = Column(String, nullable=True)
    municipality = Column(String, nullable=True)

    customer = relationship('Customer', back_populates='accounts')
    bank = relationship('Bank', back_populates='accounts')

    sent_transactions = relationship(
        'Transaction',
        foreign_keys='Transaction.sender_account',
        back_populates='sender_account_rel'
    )
    received_transactions = relationship(
        'Transaction',
        foreign_keys='Transaction.receiver_account',
        back_populates='receiver_account_rel'
    )


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

    sender_account_rel = relationship(
        'Account',
        foreign_keys=[sender_account],
        back_populates='sent_transactions'
    )
    receiver_account_rel = relationship(
        'Account',
        foreign_keys=[receiver_account],
        back_populates='received_transactions'
    )


# === Config and Logging ===

DATABASE_URL = 'postgresql+psycopg2://postgres:admin@localhost:5432/bank'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === Utility ===

def normalize_personnummer(pnr: str) -> str:
    """Normalize by removing dash and whitespace."""
    return pnr.replace("-", "").strip()


# === Functions ===

def list_customers():
    """Show the first 10 customers in the DB for inspection."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        customers = session.query(Customer).limit(10).all()
        logger.info("Listing first 10 customers in DB:")
        for c in customers:
            normalized = normalize_personnummer(c.personnummer)
            logger.info(f"Customer ID: {c.customer_id}, Raw: '{c.personnummer}', Normalized: '{normalized}'")
    finally:
        session.close()


def fix_account_customer_ids(csv_file):
    """Correct customer_id in accounts by matching normalized personnummer from CSV."""
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs all SQL commands
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Read all account-personnummer pairs from CSV
        accounts_personnummer = {}
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                account_number = row.get('BankAccount')
                personnummer = normalize_personnummer(row.get('Personnummer', ''))
                if account_number and personnummer:
                    accounts_personnummer[account_number] = personnummer

        fixed_count = 0
        for account_number, normalized_pnr in accounts_personnummer.items():
            account = session.query(Account).filter_by(account_number=account_number).first()
            if not account:
                logger.warning(f"Account {account_number} not found in DB.")
                continue

            customer = session.query(Customer).filter(
                func.replace(func.trim(Customer.personnummer), '-', '') == normalized_pnr
            ).first()

            if not customer:
                logger.warning(f"Customer with normalized personnummer '{normalized_pnr}' not found in DB.")
                continue

            if account.customer_id != customer.customer_id:
                logger.info(f"Updating account {account_number}: customer_id {account.customer_id} -> {customer.customer_id}")
                account.customer_id = customer.customer_id
                fixed_count += 1
            else:
                logger.info(f"Account {account_number} already linked to correct customer_id {customer.customer_id}")

        session.commit()
        logger.info(f"Fixed customer_id for {fixed_count} accounts.")

        # Verify changes immediately after commit
        for account_number in accounts_personnummer.keys():
            acc = session.query(Account).filter_by(account_number=account_number).first()
            if acc:
                logger.info(f"Verification - account {account_number}: customer_id={acc.customer_id}")

    except Exception as e:
        logger.error(f"Error: {e}")
        session.rollback()
    finally:
        session.close()


# === Main script ===

if __name__ == '__main__':
    csv_path = r'.\data\sebank_customers_with_accounts.csv'

    # Step 1: Show existing customers for verification
    list_customers()

    # Step 2: Fix broken customer_id references in Account table
    fix_account_customer_ids(csv_path)
