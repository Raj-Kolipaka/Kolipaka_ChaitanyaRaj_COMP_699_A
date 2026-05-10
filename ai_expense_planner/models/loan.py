class Loan:
    def __init__(self, principal, interest_rate, emi):
        self.principal = principal
        self.interest_rate = interest_rate
        self.emi = emi

    def calculate_emi(self, months):
        r = self.interest_rate / 12 / 100
        emi = (self.principal * r * (1 + r) ** months) / ((1 + r) ** months - 1)
        return emi

    def remaining_balance(self, total_paid):
        return self.principal - total_paid