
class Account:

    def __init__(self,sender_account,recevier_account):
        self.pin = ""
        self.sender_account = sender_account
        self.receiver_account = recevier_account
        self.valid = True

    def is_valid(self):
        return self.valid

    def set_pin(self, pin):
        if(self.pin == "" and len(pin) == 5):
            self.pin = pin
            return True
        else:
            return False


class Customers:
    def __init__(self,customer, address, phone, personnummer, BankAccount):
        self.customer = customer
        self.address = address
        self.phone = phone
        self.personnummer = personnummer
        self.bankAccount = BankAccount
        self.valid = True
        self.pin = ""

    def is_valid(self):
        return self.valid

    def set_pin(self, pin):
        if pin == 8:
            self.pin = pin
            return True
        else:
            return False

class Transactions:
    def __init__(self,transaction_id,timestamp,amount,currency,sender_country,
    sender_municipality,receiver_country,receiver_municipality,
    transaction_type,notes ):
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.amount= amount
        self.currency = currency
        self.sender_country = sender_country
        self.sender_municipality= sender_municipality
        self.transaction_type = transaction_type
        self.notes = notes
        self.valid = True
        self.pin = ""

        def is_valid(self):
            return self.valid

        def set_pin(self, pin):
            if pin == 6:
                self.pin = pin
                return True
            else:
                return False