from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    personnummer = Column(String, unique=True)
    email = Column(String)

    # Relationship to accounts
    accounts = relationship('Account', back_populates='customer')


class Account(Base):
    __tablename__ = 'accounts'  # renamed from 'bank_accounts'

    account_number = Column(String, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=True)

    # Relationships
    customer = relationship('Customer', back_populates='accounts')
    bank = relationship('Bank', back_populates='accounts')

    sent_transactions = relationship(
        'Transaction',
        foreign_keys='Transaction.sender_account',
        back_populates='sender_account_rel'
    )
    received_transactions = relationship(
        'Transaction',
        foreign_keys='Transaction.receiver_account',
        back_populates='receiver_account_rel'
    )


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    amount = Column(Float)
    currency = Column(String)

    sender_account = Column(String, ForeignKey('accounts.account_number'), nullable=False)
    receiver_account = Column(String, ForeignKey('accounts.account_number'), nullable=False)

    sender_country = Column(String, nullable=True)
    sender_municipality = Column(String, nullable=True)
    receiver_country = Column(String, nullable=True)
    receiver_municipality = Column(String, nullable=True)
    transaction_type = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    sender_account_rel = relationship(
        'Account',
        foreign_keys=[sender_account],
        back_populates='sent_transactions'
    )
    receiver_account_rel = relationship(
        'Account',
        foreign_keys=[receiver_account],
        back_populates='received_transactions'
    )


class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    swift_code = Column(String, unique=True)

    accounts = relationship('Account', back_populates='bank')
