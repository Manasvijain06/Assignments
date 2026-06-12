"""Question 43 : Implement encapsulation using private variables in Bank class."""

class Bank:

    def __init__(self, account_holder: str, balance: float) -> None:
        self.account_holder = account_holder
        self.__balance = balance

    def deposit(self, amount: float) -> None:
        self.__balance += amount

    def get_balance(self) -> float:
        return self.__balance


if __name__ == "__main__":
    bank_account = Bank("Manasvi", 5000)

    bank_account.deposit(1000)
    
    print(f"Balance: {bank_account.get_balance()}")