class Economy:
    def __init__(self, starting_capital=1000):
        self.money = starting_capital

    def add_money(self, amount):
        self.money += amount

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False