
class Transaction:
    def __init__(self, amount):
        self.amount = amount

    def execute(self):
        print("Processing a generic transaction...")


class Deposit(Transaction):
    
    def execute(self, note=None):
        if note:
            print(f"Deposited ${self.amount} ({note})")
        else:
            print(f"Deposited ${self.amount}")


class Withdraw(Transaction):
    
    def execute(self):
        print(f"Withdrew ${self.amount}")


class Transfer(Transaction):
    def __init__(self, amount, to_account):
        super().__init__(amount)
        self.to_account = to_account


    def execute(self):
        print(f"Transferred ${self.amount} to {self.to_account}")



print("=== Employer Actions ===")

action1 = Deposit(10000)
action1.execute() 

action2 = Deposit(500)
action2.execute("Quarterly Bonus")

action3 = Transfer(3000, "Alice (Employee)")
action3.execute()

action4 = Withdraw(100)
action4.execute()