import csv
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"


metadata = MetaData()


customers = Table(
    'customers', metadata,
    Column('customer_id', String),  # Typically this would be Integer with autoincrement
    Column('customer_name', String),
    Column('address', String),
    Column('phone', String),
    Column('personnummer', String, unique=True),
    Column('email', String)
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

try:
    with open(r'./cleaned_customers.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        connection = engine.connect()
        trans = connection.begin()
        try:
            for row in reader:
                insert_stmt = insert(customers).values(
                    customer_name=row['Customer'],
                    address=row['Address'],
                    phone=row['Phone'],
                    personnummer=row['Personnummer'],
                    email=row.get('Email')
                )
                do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['personnummer'])
                connection.execute(do_nothing_stmt)
            trans.commit()
            print("All records inserted successfully (duplicates skipped).")
        except Exception as e:
            trans.rollback()
            print(f"Transaction rolled back due to: {e}")
        finally:
            connection.close()

except (SQLAlchemyError, IOError) as e:
    print(f"Error occurred: {e}")
