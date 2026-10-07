# Где находится balance?
# Почему get_balance() продолжает его видеть после завершения make_account()?
# Зачем здесь nonlocal?
# Что будет, если убрать nonlocal?


def make_account(owner, initial_balance):
    balance = initial_balance

    def deposit(amount):
        nonlocal balance
        balance += amount

    def get_balance():
        return balance

    return deposit, get_balance


deposit, get_balance = make_account("Alice", 100)

deposit(50)
deposit(25)

print(get_balance())


