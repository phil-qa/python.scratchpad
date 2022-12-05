class BankAccount():
    def __init__(self, account_name, account_number, account_balance):
        self.account_name = account_name
        self.account_number = account_number
        self.account_balance = account_balance

    def make_deposit(self, value):
        self.account_balance += value

    def make_withdrawal(self,value):
        self.account -= value

    def show_balance(self):
        print(f"balance {self.account_balance}")

