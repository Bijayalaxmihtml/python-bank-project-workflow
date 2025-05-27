import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer  # assuming your models are in models.py

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/bank"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def import_customers(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing = session.query(Customer).filter_by(personnummer=row['personnummer']).first()
            if existing:
                print(f"Customer {row['personnummer']} already exists, skipping.")
                continue

            customer = Customer(
                customer_name=row['customer_name'],
                address=row.get('address'),
                phone=row.get('phone'),
                personnummer=row['personnummer'],
                email=row.get('email'),
            )
            session.add(customer)
            print(f"Added customer {row['personnummer']}")

        session.commit()
        print("Customer import done.")

if __name__ == '__main__':
    import_customers('customers.csv')
