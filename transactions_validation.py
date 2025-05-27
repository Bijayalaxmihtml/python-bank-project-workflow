import re
import pandas as pd
from pydantic import BaseModel, field_validator, ValidationError
from typing import List

# Paths
CSV_PATH = r".\data\transactions_original.csv"
OUTPUT_CLEAN_PATH = r".\data\transactions_cleaned.csv"
OUTPUT_INVALID_PATH = r".\data\transactions_invalid.csv"

def clean_iban(iban):
    """Remove spaces/dashes, uppercase IBAN."""
    if not isinstance(iban, str):
        return ""
    return iban.replace(" ", "").replace("-", "").strip().upper()

def is_valid_swedish_iban(iban: str) -> bool:
    """Validate Swedish IBAN: SE + 22 alphanumeric uppercase chars."""
    iban = clean_iban(iban)
    return bool(re.fullmatch(r"SE[0-9A-Z]{22}", iban))

class Transaction(BaseModel):
    sender_account: str
    receiver_account: str
    currency: str

    @field_validator("sender_account")
    @classmethod
    def validate_sender_account(cls, v):
        if not is_valid_swedish_iban(v):
            raise ValueError("Invalid Swedish bank account number")
        return clean_iban(v)

    @field_validator("receiver_account")
    @classmethod
    def validate_receiver_account(cls, v):
        if not is_valid_swedish_iban(v):
            raise ValueError("Invalid Swedish bank account number")
        return clean_iban(v)

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        if not isinstance(v, str) or v.strip().upper() != "SEK":
            raise ValueError("Currency must be SEK")
        return "SEK"

def validate_transactions():
    print(" Loading CSV...")
    df = pd.read_csv(CSV_PATH, dtype={"sender_account": str, "receiver_account": str}, low_memory=False)
    print(f" Loaded {len(df)} transactions.")

    valid_rows: List[dict] = []
    invalid_rows = {}

    print(" Validating transactions...")

    for idx, row in df.iterrows():
        data = {
            "sender_account": row.get("sender_account", ""),
            "receiver_account": row.get("receiver_account", ""),
            "currency": row.get("currency", ""),
        }
        try:
            Transaction(**data)
            valid_rows.append(row)
        except ValidationError as e:
            invalid_rows[idx] = e.errors()

    invalid_sender = sum(any(err["loc"][0] == "sender_account" for err in errs) for errs in invalid_rows.values())
    invalid_receiver = sum(any(err["loc"][0] == "receiver_account" for err in errs) for errs in invalid_rows.values())
    invalid_currency = sum(any(err["loc"][0] == "currency" for err in errs) for errs in invalid_rows.values())

    print("\n Validation Summary:")
    print(f" - Invalid sender_account: {invalid_sender}")
    print(f" - Invalid receiver_account: {invalid_receiver}")
    print(f" - Invalid currency: {invalid_currency}")
    print(f" - Total valid rows: {len(valid_rows)}")
    print(f" - Total invalid rows: {len(invalid_rows)}")

    # Save valid transactions
    cleaned_df = pd.DataFrame(valid_rows)
    cleaned_df.to_csv(OUTPUT_CLEAN_PATH, index=False)
    print(f"\n Cleaned valid data saved to: {OUTPUT_CLEAN_PATH}")

    # Save invalid transactions
    invalid_df = df.loc[invalid_rows.keys()]
    invalid_df.to_csv(OUTPUT_INVALID_PATH, index=False)
    print(f" Invalid transactions saved to: {OUTPUT_INVALID_PATH}")

    # Show sample errors
    print("\n Sample invalid IBANs and errors:")
    for idx in list(invalid_rows.keys())[:10]:  # limit output
        row = df.loc[idx]
        sender = row.get("sender_account", "")
        receiver = row.get("receiver_account", "")
        errs = invalid_rows[idx]
        err_msgs = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in errs)
        print(f"Row {idx} - Sender: {sender}, Receiver: {receiver} | Errors: {err_msgs}")

if __name__ == "__main__":
    validate_transactions()
