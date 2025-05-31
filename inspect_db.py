from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Account, Transaction, Bank  # Adjust if needed

# DB credentials
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank"  # your real DB name

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def print_table(name, records):
    print(f"\n========== {name.upper()} ==========")
    if records:
        for r in records:
            print({c.name: getattr(r, c.name) for c in r.__table__.columns})
    else:
        print("No records found.")

def main():
    with Session() as session:
        print_table("accounts", session.query(Account).all())
        print_table("customers", session.query(Customer).all())
        print_table("transactions", session.query(Transaction).all())
        print_table("banks", session.query(Bank).all())

if __name__ == "__main__":
    main()
