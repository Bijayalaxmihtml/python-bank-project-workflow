import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator
import re

CUSTOMERS_CSV_PATH = r"./data/sebank_customers_with_accounts_original.csv"

def luhn_checksum(num_str: str) -> bool:
    """
    Calculate Luhn checksum for Swedish personnummer (without century)
    and validate it.
    """
    digits = [int(d) for d in num_str]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 0:
            doubled = d * 2
            total += doubled if doubled < 10 else doubled - 9
        else:
            total += d
    return total % 10 == 0

class Customer(BaseModel):
    name: str
    address: str
    phone: str
    personnummer: str
    bank_account: str

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        if not isinstance(v, str) or not re.match(r'^\+?[\d\s\-\(\)]+$', v):
            raise ValueError('Invalid phone number format')
        # Normalize phone by removing spaces and dashes
        normalized = re.sub(r'[\s\-]', '', v)
        return normalized

    @field_validator('personnummer')
    def validate_personnummer(cls, v):
        if not isinstance(v, str) or not re.match(r'^\d{6}[-+]\d{4}$', v):
            raise ValueError('Invalid personnummer format')
        # Remove separator to get digits only for checksum
        digits_only = v.replace("-", "").replace("+", "")
        if not luhn_checksum(digits_only):
            raise ValueError('Personnummer failed checksum validation')
        return v

    @field_validator('bank_account')
    def validate_bank_account(cls, v):
        if not isinstance(v, str):
            raise ValueError('Bank account must be a string')
        # Clean IBAN first: remove spaces/dashes and uppercase
        clean_v = re.sub(r'[^0-9A-Za-z]', '', v).upper()
        if not (clean_v.startswith('SE') and len(clean_v) == 24):
            raise ValueError('Invalid Swedish bank account number')
        return clean_v


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
            errors.append((idx + 2, e.errors()))  # +2 for header + 0-based idx

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
