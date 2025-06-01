Python bank project
In this project, we have a banking system that processes a set number of transactions. Some of these transactions contain faulty data, such as incorrect dates, potential fraud, or other suspicious activity. We've been managing the data flow through testing, validation, and migrations, supported by a functional rollback mechanism and workflow management system.

We've written tests using Pytest to ensure the functionality of the banking system. For data validation and modeling, we've used Pydantic, helping us maintain clean, structured and validated data. We've also set up a database to make the data easy to read and work with. On top of that, we've implemented an automated workflow using Prefect Cloud to streamline the entire process.

To ensure a smooth installation of all necessary packages, we used the requirements.txt file.

Files
We have a number of folders containing files we have used but we also have loose files.

Data:
You'll find all transactions that are invalid, cleaned and a orginal copy of said file. You will also find customer data that are cleaned. - clean_transactions_pipeline.py - cleaned_customers.csv - cleaned_transactions.csv - explore_data.py - import_customers.py - sebank_customers_with_accounts.csv - suspicious_transactions.csv - transactions.csv - transactions_cleaned.csv - transactions_invalid.csv - transactions_orginal.csv

Alembic
This folder is containing our configuration for Alembic.

Venv
Our environment

List of loose files
alembic.ini
.gitigoner
bank.db
bank_workflow.py
customer_validation.py
bank_workflow.py
create_tables.py
fix_account_customer_ids.py
import_banks.py
import_banks_from_accounts.py
inspect_db.py
requirements.txt
rollback_and_reimport_postgres.py
import_accounts.py
import_missing_accounts.py
import_transactions.py
models.py
transactions_validation.py
valid_customers.csv
insert_customers_postgres.py
inspect.py
test.py
Benjamin's github containing bank application
account.py
app.py
bank.py
creat_db_sql
customer.py
db.py
interest,py
manager.py
officer.py
transaction.py
validate_transactions.ipynb
Contributors for this project:
IsraDirie - Isra Dirie
Bijayalaxmihtml - Bijayalaxmi Dash (Laxmi)
MarcoKJNilsson - Marco Nilsson

