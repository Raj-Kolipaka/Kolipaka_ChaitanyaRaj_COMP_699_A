from flask import Blueprint, request, redirect, session, render_template
from services.expense_service import ExpenseService

expense_bp = Blueprint('expense', __name__)

expense_service = ExpenseService()


# -------- VIEW EXPENSE PAGE --------
@expense_bp.route('/expenses')
def view_expenses():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    expenses = expense_service.get_all_expenses(user_id)

    return render_template('expenses.html', expenses=expenses)


# -------- ADD EXPENSE --------
@expense_bp.route('/add_expense', methods=['POST'])
def add_expense():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    amount = float(request.form['amount'])
    category = request.form['category']

    expense_service.add_expense(user_id, amount, category)

    return redirect('/expenses')


# -------- DELETE EXPENSE --------
@expense_bp.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):

    if 'user_id' not in session:
        return redirect('/login')

    expense_service.delete_expense(expense_id)

    return redirect('/expenses')