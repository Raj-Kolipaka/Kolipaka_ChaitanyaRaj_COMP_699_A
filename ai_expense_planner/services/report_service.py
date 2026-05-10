from database.models import User, Expense, Loan
from database.db import db


class ReportService:

    # -------- SYSTEM REPORT --------
    def generate_system_report(self):

        try:
            total_users = User.query.count()

            total_expenses = db.session.query(
                db.func.sum(Expense.amount)
            ).scalar()

            if total_expenses is None:
                total_expenses = 0

            total_loans = Loan.query.count()

            return {
                "total_users": total_users,
                "total_expenses": round(total_expenses, 2),
                "total_loans": total_loans
            }

        except Exception as e:
            print("Report Error:", e)

            return {
                "total_users": 0,
                "total_expenses": 0,
                "total_loans": 0
            }