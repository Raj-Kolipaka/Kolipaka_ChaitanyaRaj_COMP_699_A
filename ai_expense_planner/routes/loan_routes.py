from flask import Blueprint, request, redirect, session, render_template
from services.loan_service import LoanService

loan_bp = Blueprint('loan', __name__)

loan_service = LoanService()


# -------- VIEW LOAN PAGE --------
@loan_bp.route('/loan')
def view_loan():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    loan = loan_service.get_loan(user_id)

    return render_template('loans.html', loan=loan)


# -------- CREATE LOAN --------
@loan_bp.route('/create_loan', methods=['POST'])
def create_loan():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    principal = float(request.form['principal'])
    interest_rate = float(request.form['interest_rate'])
    emi = float(request.form['emi'])

    loan_service.create_loan(user_id, principal, interest_rate, emi)

    return redirect('/loan')


# -------- PAY EMI --------
@loan_bp.route('/pay_emi')
def pay_emi():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    loan_service.mark_emi_paid(user_id)

    return redirect('/loan')