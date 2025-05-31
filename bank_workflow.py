from prefect import flow, task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Transaction
from typing import List


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@task
def fetch_customer_personnummers(limit: int = 30) -> List[str]:
    with SessionLocal() as session:
        customers = session.query(Customer).limit(limit).all()
        return [c.personnummer for c in customers if c.personnummer]


@task
def process_customer_transactions(personnummer: str) -> str:
    with SessionLocal() as session:
        # Find customer by personnummer
        customer = session.query(Customer).filter(Customer.personnummer == personnummer).first()
        if not customer:
            return f"No customer found for {personnummer}"

        # Get all account numbers for this customer
        accounts = [account.account_number for account in customer.accounts]
        if not accounts:
            return f"Customer {personnummer} has no accounts"

        # Count sent and received transactions
        sent_count = session.query(Transaction).filter(Transaction.sender_account.in_(accounts)).count()
        received_count = session.query(Transaction).filter(Transaction.receiver_account.in_(accounts)).count()

        return (
            f"Customer {personnummer}: "
            f"{len(accounts)} accounts, "
            f"{sent_count} sent transactions, "
            f"{received_count} received transactions"
        )


@flow
def banking_etl_flow():
    personnummers = fetch_customer_personnummers()
    results = process_customer_transactions.map(personnummers)
    for res in results:
        print(res)


if __name__ == "__main__":
    banking_etl_flow()
