from flask import Flask, redirect
from config import Config
from database.db import db

# import routes
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.expense_routes import expense_bp
from routes.loan_routes import loan_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init db
    db.init_app(app)

    # register routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(admin_bp)

    # create DB tables
    with app.app_context():
        db.create_all()

    # -------- HOME ROUTE (FIX) --------
    @app.route('/')
    def home():
        return redirect('/login')

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)