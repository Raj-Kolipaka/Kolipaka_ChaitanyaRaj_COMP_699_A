from flask import Blueprint, session, redirect, render_template, request
from services.report_service import ReportService
from database.models import User

admin_bp = Blueprint('admin', __name__)

report_service = ReportService()


# -------- ADMIN DASHBOARD --------
@admin_bp.route('/admin/dashboard')
def admin_dashboard():

    #  Access control
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    #  Get system report
    report = report_service.generate_system_report()

    #  fallback (safety)
    if not report:
        report = {
            "total_users": 0,
            "total_expenses": 0,
            "total_loans": 0
        }

    return render_template('admin_dashboard.html', report=report)


# -------- VIEW ALL USERS --------
@admin_bp.route('/admin/users')
def view_users():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    users = User.query.all()

    return render_template('admin_users.html', users=users)


# -------- SYSTEM REPORT PAGE --------
@admin_bp.route('/admin/reports')
def admin_reports():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    report = report_service.generate_system_report()

    return render_template('admin_reports.html', report=report)


# -------- LOGOUT (ADMIN) --------
@admin_bp.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/login')