import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# === CONFIG ===
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}

CUSTOMERS_TABLE = 'customers'
TRANSACTIONS_TABLE = 'transactions'

CUSTOMERS_CSV = 'valid_customers.csv'
TRANSACTIONS_CSV = './data/transactions_cleaned.csv'

# === CONNECT TO POSTGRES ===
print("🔌 Connecting to PostgreSQL...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
print("✅ Connected.\n")

# === DELETE EXISTING DATA (ROLLBACK) ===
print("🧹 Deleting old data from tables...")
cursor.execute(f'DELETE FROM {TRANSACTIONS_TABLE};')
cursor.execute(f'DELETE FROM {CUSTOMERS_TABLE};')
conn.commit()
print("✅ Old data deleted.\n")

# === LOAD CLEANED DATA ===
print("📂 Loading cleaned CSVs...")
customers_df = pd.read_csv(CUSTOMERS_CSV)
transactions_df = pd.read_csv(TRANSACTIONS_CSV)
print(f"✅ Loaded {len(customers_df)} customers and {len(transactions_df)} transactions.\n")

# === FUNCTION TO BULK INSERT ===
def bulk_insert(df, table_name, cursor):
    cols = ', '.join(df.columns)
    values = [tuple(x) for x in df.to_numpy()]
    insert_query = f"INSERT INTO {table_name} ({cols}) VALUES %s"
    execute_values(cursor, insert_query, values)

# === INSERT DATA ===
print("📥 Inserting cleaned customers...")
bulk_insert(customers_df, CUSTOMERS_TABLE, cursor)

print("📥 Inserting cleaned transactions...")
bulk_insert(transactions_df, TRANSACTIONS_TABLE, cursor)

conn.commit()
print("✅ Clean data re-imported successfully.\n")

# === CLOSE CONNECTION ===
cursor.close()
conn.close()
print("🔒 PostgreSQL connection closed.")
