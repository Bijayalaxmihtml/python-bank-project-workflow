import logging
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"

# Setup engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()  # no bind argument here

# Define banks table (must match your actual table schema)
banks = Table(
    'banks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('address', String),
    Column('swift_code', String, unique=True)
)

accounts = Table(
    'accounts', metadata,
    Column('account_number', String, primary_key=True),
    Column('customer_id', Integer),
    Column('bank_id', Integer),
    Column('country', String),
    Column('municipality', String)
)

try:
    # Get distinct bank_id values from accounts table where bank_id is not null
    distinct_bank_ids = session.execute(
        select(accounts.c.bank_id).distinct().where(accounts.c.bank_id != None)
    ).scalars().all()

    logger.info(f"Found bank IDs in accounts: {distinct_bank_ids}")

    # For each bank_id, we should get bank info from somewhere
    # Since you said you do not have banks CSV,
    # here we will create dummy bank names based on bank_id for demo
    for bank_id in distinct_bank_ids:
        # Check if bank already exists in banks table
        bank_exists = session.execute(
            select(banks).where(banks.c.id == bank_id)
        ).first()

        if bank_exists:
            logger.info(f"Bank with id {bank_id} already exists. Skipping insert.")
            continue

        # Insert dummy bank data, replace this with real data if you have it
        ins = insert(banks).values(
            id=bank_id,
            name=f"Bank {bank_id}",
            address=None,
            swift_code=None
        )
        session.execute(ins)
        logger.info(f"Inserted Bank with id {bank_id}")

    session.commit()
    logger.info("All banks inserted successfully.")

except Exception as e:
    logger.error(f"Error during bank import: {e}")
    session.rollback()
finally:
    session.close()
