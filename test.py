import pytest

def test_sender_account_length():
    sender_account = "SE8902EWFT80524424320740"
    assert len(sender_account) == 24

def test_receiver_account_length():
    receiver_account = "SE8902ZUIH32054423564254"
    assert len(receiver_account) == 24

def test_transaction_id():
    transaction_id = "f2f3b0fc-b7d7-4d85-b682-cbf07ef77c1a"
    return transaction_id

def test_timestamp():
    timestamp= "2025-03-06 12:04:00"
    return timestamp

def test_amount_():
    amount= 7746.03
    assert amount >=0

def test_currency():
    currency = "sek"
    return currency


def test_sender_country():
    sender_country= "Sweden"
    return sender_country

def test_sender_municipality():
    sender_municipality= "Karlskrona"
    return sender_municipality

def test_receiver_country():
    receiver_country= "Sweden"
    return receiver_country

def test_receiver_municipality():
    recevier_municipality= "Eskilstuna"
    return recevier_municipality

def test_transaction_type():
    transaction_type= "outgoing"
    return transaction_type

def test_notes():
    notes= "Online purchase"
    return notes

def test_customer():
    customer= "Kristina Blomberg"
    return customer

def test_address():
    address = "Ringvägen 06, 64659 Kalmar"
    return address


def test_phone_number():
    phone_number= "099-22 72 57"
    return phone_number

def test_personnummer():
    personnummer= "591202-5292"
    return personnummer

def test_BankAccount():
    BankAccount= "SE8902XIMR45726412027481"
    return BankAccount



