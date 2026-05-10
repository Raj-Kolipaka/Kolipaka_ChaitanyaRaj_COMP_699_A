from database.models import User
from database.db import db


class AuthService:

    # -------- REGISTER --------
    def register_user(self, name, email, password, role="student"):

        existing = User.query.filter_by(email=email).first()

        if existing:
            return {"status": False, "message": "User already exists"}

        new_user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return {"status": True, "message": "User registered successfully"}


    # -------- LOGIN --------
    def login_user(self, email, password):

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"status": False, "message": "User not found"}

        # check password separately
        if user.password != password:
            return {"status": False, "message": "Incorrect password"}

        return {
            "status": True,
            "user_id": user.id,
            "role": user.role,
            "name": user.name
        }


    # -------- GET USER --------
    def get_user(self, user_id):
        return User.query.get(user_id)