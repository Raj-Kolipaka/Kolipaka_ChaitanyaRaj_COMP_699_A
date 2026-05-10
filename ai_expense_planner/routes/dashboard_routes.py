from flask import Blueprint, render_template, session, redirect, request
from services.planner_system import PlannerSystem
from services.report_service import ReportService
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

planner = PlannerSystem()
report_service = ReportService()


# -------- DASHBOARD --------
@dashboard_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    #  dynamic date (FIXED)
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # summaries
    monthly = planner.get_monthly_summary(user_id, current_month, current_year)
    yearly = planner.get_yearly_summary(user_id, current_year)

    # loan data
    progress = planner.loan_progress(user_id)
    duration = planner.loan_duration(user_id)

    # ML
    prediction = planner.predict_expense(user_id)
    suggestions = planner.get_suggestions(user_id)

    # notifications
    planner.check_reminders(user_id)
    notifications = planner.get_notifications(user_id)

    return render_template(
        'dashboard.html',
        monthly=monthly,
        yearly=yearly,
        progress=progress,
        duration=duration,
        prediction=prediction,
        suggestions=suggestions,
        notifications=notifications
    )


# -------- REPORTS PAGE --------
@dashboard_bp.route('/reports')
def reports():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    month = request.args.get('month')
    year = request.args.get('year')
    year_only = request.args.get('year_only')

    monthly_report = None
    yearly_report = None

    if month and year:
        monthly_report = report_service.monthly_report(
            user_id, int(month), int(year)
        )

    if year_only:
        yearly_report = report_service.yearly_report(
            user_id, int(year_only)
        )

    return render_template(
        'reports.html',
        monthly_report=monthly_report,
        yearly_report=yearly_report
    )


# -------- EXPORT REPORT --------
@dashboard_bp.route('/export_report')
def export_report():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    year = request.args.get('year')

    if not year:
        return "Please provide year"

    data = report_service.export_yearly_report(user_id, int(year))

    return f"<pre>{data}</pre>"