from services.expense_service import ExpenseService
from services.loan_service import LoanService
from services.ml_service import MLService
from services.report_service import ReportService
from services.notification_service import NotificationService


class PlannerSystem:

    def __init__(self):
        self.expense_service = ExpenseService()
        self.loan_service = LoanService()
        self.ml_service = MLService()
        self.report_service = ReportService()
        self.notification_service = NotificationService()


    # -------- EXPENSE FLOW --------
    def add_expense(self, user_id, amount, category):
        return self.expense_service.add_expense(user_id, amount, category)


    def get_monthly_summary(self, user_id, month, year):
        return self.expense_service.get_monthly_summary(user_id, month, year)


    def get_yearly_summary(self, user_id, year):
        return self.expense_service.get_yearly_summary(user_id, year)


    # -------- LOAN FLOW --------
    def create_loan(self, user_id, principal, interest_rate, emi):
        return self.loan_service.create_loan(user_id, principal, interest_rate, emi)


    def pay_emi(self, user_id):
        return self.loan_service.mark_emi_paid(user_id)


    def loan_progress(self, user_id):
        return self.loan_service.calculate_progress(user_id)


    def loan_duration(self, user_id):
        return self.loan_service.estimate_loan_duration(user_id)


    def interest_saved(self, user_id, extra_payment):
        return self.loan_service.estimate_interest_saved(user_id, extra_payment)


    # -------- ML FLOW --------
    def train_model(self, user_id):
        return self.ml_service.train_model(user_id)


    def predict_expense(self, user_id):
        return self.ml_service.predict_next(user_id)


    def get_suggestions(self, user_id):
        return self.ml_service.generate_suggestions(user_id)


    # -------- REPORT FLOW --------
    def monthly_report(self, user_id, month, year):
        return self.report_service.monthly_report(user_id, month, year)


    def yearly_report(self, user_id, year):
        return self.report_service.yearly_report(user_id, year)


    def export_report(self, user_id, year):
        return self.report_service.export_yearly_report(user_id, year)


    # -------- NOTIFICATION FLOW --------
    def get_notifications(self, user_id):
        return self.notification_service.get_notifications(user_id)


    def check_reminders(self, user_id):
        self.notification_service.check_emi_reminder(user_id)


    # -------- FULL PLAN GENERATION --------
    def generate_plan(self, user_id):
        prediction = self.predict_expense(user_id)
        suggestions = self.get_suggestions(user_id)
        progress = self.loan_progress(user_id)

        return {
            "predicted_expense": prediction,
            "suggestions": suggestions,
            "loan_progress": progress
        }