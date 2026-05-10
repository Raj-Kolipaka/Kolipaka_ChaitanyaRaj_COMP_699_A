from flask import Blueprint, render_template, request, redirect, session
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

auth_service = AuthService()


# -------- REGISTER --------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # validation
        if not name or not email or not password:
            return render_template("register.html", message="All fields are required")

        result = auth_service.register_user(name, email, password)

        if result["status"]:
            return render_template("login.html", message="Registration successful. Please login.")
        else:
            return render_template("register.html", message=result["message"])

    return render_template('register.html')


# -------- LOGIN --------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        # validation
        if not email or not password:
            return render_template("login.html", message="Please enter email and password")

        result = auth_service.login_user(email, password)

        if result["status"]:
            session['user_id'] = result["user_id"]
            session['role'] = result["role"]

            if result["role"] == "admin":
                return redirect('/admin/dashboard')
            else:
                return redirect('/dashboard')

        return render_template("login.html", message="Invalid email or password")

    return render_template('login.html')


# -------- LOGOUT --------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')