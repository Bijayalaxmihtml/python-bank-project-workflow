import pandas as pd

# Update the paths to your CSV files
transactions_path = r"./transactions.csv"
customers_path = r"./sebank_customers_with_accounts.csv"

# Load CSV data into DataFrames
transactions = pd.read_csv(transactions_path)
customers = pd.read_csv(customers_path)

# Quick look at the data
print(transactions.head())
print(customers.head())

# Summary info
print(transactions.info())
print(customers.info())

print("Missing values in transactions:")
print(transactions.isnull().sum())

print("\nMissing values in customers:")
print(customers.isnull().sum())

print("\nDuplicate transaction IDs:")
print(transactions['transaction_id'].duplicated().sum())

print("\nDuplicate bank accounts in customers:")
print(customers['BankAccount'].duplicated().sum())

print("\nTransaction amounts stats:")
print(transactions['amount'].describe())

# Optional: filter suspicious transactions with negative or zero amounts
suspicious = transactions[transactions['amount'] <= 0]
print(f"\nSuspicious transactions with non-positive amounts:\n{suspicious}")
