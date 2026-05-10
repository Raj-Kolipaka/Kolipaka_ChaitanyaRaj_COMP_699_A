from database.models import Loan
from database.db import db


class LoanService:

    def create_loan(self, user_id, principal, interest_rate, emi_amount):
        loan = Loan(
            user_id=user_id,
            principal=principal,
            interest_rate=interest_rate,
            emi_amount=emi_amount,
            balance=principal,
            total_paid=0
        )

        db.session.add(loan)
        db.session.commit()

        return {"status": True, "message": "Loan created"}


    def get_loan(self, user_id):
        return Loan.query.filter_by(user_id=user_id).first()


    def mark_emi_paid(self, user_id):
        loan = Loan.query.filter_by(user_id=user_id).first()

        if not loan:
            return {"status": False, "message": "Loan not found"}

        loan.total_paid += loan.emi_amount
        loan.balance -= loan.emi_amount

        if loan.balance < 0:
            loan.balance = 0

        db.session.commit()

        return {
            "status": True,
            "message": "EMI recorded",
            "balance": loan.balance
        }


    def calculate_progress(self, user_id):
        loan = Loan.query.filter_by(user_id=user_id).first()

        if not loan:
            return 0

        total = loan.principal
        paid = loan.total_paid

        progress = (paid / total) * 100 if total > 0 else 0

        return round(progress, 2)


    def estimate_loan_duration(self, user_id):
        loan = Loan.query.filter_by(user_id=user_id).first()

        if not loan:
            return 0

        if loan.emi_amount == 0:
            return 0

        months = loan.balance / loan.emi_amount

        return round(months)


    def estimate_interest_saved(self, user_id, extra_payment):
        loan = Loan.query.filter_by(user_id=user_id).first()

        if not loan:
            return 0

        standard_months = loan.balance / loan.emi_amount
        new_months = loan.balance / (loan.emi_amount + extra_payment)

        saved_months = standard_months - new_months

        return round(saved_months, 2)