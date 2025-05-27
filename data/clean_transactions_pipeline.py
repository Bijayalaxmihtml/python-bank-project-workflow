import pandas as pd

# ✅ Full file paths (Make sure these files exist at these exact locations)
transactions_path = r"./transactions.csv"
customers_path = r"C:./sebank_customers_with_accounts.csv"

# Load data
transactions = pd.read_csv(transactions_path)
customers = pd.read_csv(customers_path)

# Overview
print("Initial transactions shape:", transactions.shape)
print("Initial customers shape:", customers.shape)

# Handle Duplicates - Transactions
transactions_before = transactions.shape[0]
transactions = transactions.drop_duplicates(subset='transaction_id')
print(f"Removed {transactions_before - transactions.shape[0]} duplicate transactions.")

# Handle Suspicious Amounts - Transactions
suspicious = transactions[transactions['amount'] <= 0]
print(f"Found {suspicious.shape[0]} suspicious transactions with non-positive amounts.")
suspicious.to_csv(r"./suspicious_transactions.csv", index=False)
transactions = transactions[transactions['amount'] > 0]

# Handle Missing Values - Transactions
print("\nTransactions missing values BEFORE handling:")
print(transactions.isnull().sum())

critical_fields = ['transaction_id', 'amount', 'currency', 'timestamp']
transactions = transactions.dropna(subset=critical_fields)

if 'merchant_name' in transactions.columns:
    transactions['merchant_name'] = transactions['merchant_name'].fillna("Unknown")

for col in ['sender_country', 'sender_municipality', 'receiver_country', 'receiver_municipality']:
    if col in transactions.columns:
        transactions[col] = transactions[col].fillna("Unknown")

if 'notes' in transactions.columns:
    transactions['notes'] = transactions['notes'].fillna("")

print("\nTransactions missing values AFTER handling:")
print(transactions.isnull().sum())

# Handle Duplicates - Customers
customers_before = customers.shape[0]
customers = customers.drop_duplicates(subset=['Personnummer', 'BankAccount'])
print(f"\nRemoved {customers_before - customers.shape[0]} duplicate customer records.")

# Handle Missing Values - Customers
print("\nCustomers missing values BEFORE handling:")
print(customers.isnull().sum())

for col in ['Phone', 'Address']:
    if col in customers.columns:
        customers[col] = customers[col].fillna("Unknown")

critical_customer_fields = ['Customer', 'Personnummer', 'BankAccount']
customers = customers.dropna(subset=critical_customer_fields)

print("\nCustomers missing values AFTER handling:")
print(customers.isnull().sum())

# Save Cleaned Data
cleaned_transactions_path = r"./cleaned_transactions.csv"
transactions.to_csv(cleaned_transactions_path, index=False)
print(f"\nCleaned transactions saved to:\n{cleaned_transactions_path}")

cleaned_customers_path = r"./cleaned_customers.csv"
customers.to_csv(cleaned_customers_path, index=False)
print(f"Cleaned customers saved to:\n{cleaned_customers_path}")
