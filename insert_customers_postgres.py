import csv
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

# PostgreSQL connection URL
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/bank"

# Define table metadata
metadata = MetaData()

# Define the customers table structure
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

# Define the path to your CSV file
csv_file_path = r'.\data\cleaned_customers.csv'

# Start the connection and handle transaction manually
connection = engine.connect()
transaction = connection.begin()

try:
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            insert_stmt = insert(customers).values(
                customer_name=row['Customer'],
                address=row['Address'],
                phone=row['Phone'],
                personnummer=row['Personnummer'],
                email=row.get('Email')
            )
            # Prevent duplicate personnummer entries
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['personnummer'])
            connection.execute(do_nothing_stmt)

    # Commit the transaction if all insertions succeed
    transaction.commit()
    print("All records inserted successfully (duplicates skipped).")

except (SQLAlchemyError, IOError) as e:
    print(f"Error occurred: {e}")
    transaction.rollback()
finally:
    connection.close()
