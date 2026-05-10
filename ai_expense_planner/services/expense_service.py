from database.models import Expense
from database.db import db
from datetime import datetime
from sqlalchemy import extract


class ExpenseService:

    def add_expense(self, user_id, amount, category):
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            date=datetime.utcnow()
        )

        db.session.add(expense)
        db.session.commit()

        return {"status": True, "message": "Expense added"}


    def edit_expense(self, expense_id, amount, category):
        expense = Expense.query.get(expense_id)

        if not expense:
            return {"status": False, "message": "Expense not found"}

        expense.amount = amount
        expense.category = category

        db.session.commit()

        return {"status": True, "message": "Expense updated"}


    def delete_expense(self, expense_id):
        expense = Expense.query.get(expense_id)

        if not expense:
            return {"status": False, "message": "Expense not found"}

        db.session.delete(expense)
        db.session.commit()

        return {"status": True, "message": "Expense deleted"}


    def get_monthly_summary(self, user_id, month, year):
        expenses = Expense.query.filter(
            Expense.user_id == user_id,
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).all()

        total = sum(e.amount for e in expenses)

        return {
            "total": total,
            "count": len(expenses)
        }


    def get_yearly_summary(self, user_id, year):
        expenses = Expense.query.filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year
        ).all()

        total = sum(e.amount for e in expenses)

        return {
            "total": total,
            "count": len(expenses)
        }


    def get_all_expenses(self, user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()

        data = []
        for e in expenses:
            data.append({
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "date": e.date
            })

        return data