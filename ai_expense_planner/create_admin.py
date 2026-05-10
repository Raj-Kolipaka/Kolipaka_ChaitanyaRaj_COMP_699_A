from app import app
from database.db import db
from database.models import User


def create_admin():
    with app.app_context():

        # check if admin already exists
        existing = User.query.filter_by(email="kolipaka123@gmail.com").first()

        if existing:
            print(" Admin already exists!")
            return

        admin = User(
            name="Admin",
            email="kolipaka123@gmail.com",
            password="kolipaka123",
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")


if __name__ == "__main__":
    create_admin()