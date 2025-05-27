import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator
import re

CUSTOMERS_CSV_PATH = r"./data/sebank_customers_with_accounts_original.csv"


class Customer(BaseModel):
    name: str
    address: str
    phone: str
    personnummer: str
    bank_account: str

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        # Accept digits, spaces, dashes, plus, parentheses for phone numbers
        if not re.match(r'^\+?[\d\s\-\(\)]+$', v):
            raise ValueError('Invalid phone number format')
        return v

    @field_validator('personnummer')
    def validate_personnummer(cls, v):
        # Swedish personal identity number format e.g. 400118-5901 or 400118+5901
        if not re.match(r'^\d{6}[-+]\d{4}$', v):
            raise ValueError('Invalid personnummer format')
        return v

    @field_validator('bank_account')
    def validate_bank_account(cls, v):
        # Basic check: starts with 'SE' and length is 24 characters (IBAN format for Sweden)
        if not (v.startswith('SE') and len(v) == 24):
            raise ValueError('Invalid Swedish bank account number')
        return v


def validate_customers():
    print(" Validating Customers...")

    # Load CSV into DataFrame
    df = pd.read_csv(CUSTOMERS_CSV_PATH)

    # Rename CSV columns to match Pydantic model fields
    df = df.rename(columns={
        "Customer": "name",
        "Address": "address",
        "Phone": "phone",
        "Personnummer": "personnummer",
        "BankAccount": "bank_account"
    })

    errors = []
    valid_customers = []

    for idx, row in df.iterrows():
        try:
            customer = Customer(**row.to_dict())
            valid_customers.append(customer)
        except ValidationError as e:
            # +2 to account for header and 0-index difference in row number
            errors.append((idx + 2, e.errors()))

    print(f" Validated {len(valid_customers)} customers successfully.")

    # Save valid customers to CSV
    if valid_customers:
        pd.DataFrame([c.model_dump() for c in valid_customers]).to_csv("valid_customers.csv", index=False)
        print(" Saved valid customers to 'valid_customers.csv'")

    # Save validation errors log if any
    if errors:
        print(f"\n Found errors in {len(errors)} rows:")
        with open("validation_errors.log", "w") as f:
            for idx, err in errors:
                print(f"Row {idx} errors:")
                f.write(f"Row {idx} errors:\n")
                for e in err:
                    msg = f" - {e['loc'][0]}: {e['msg']}"
                    print(msg)
                    f.write(msg + "\n")
                print()
                f.write("\n")
        print("📝 Saved detailed error log to 'validation_errors.log'")


if __name__ == "__main__":
    validate_customers()

