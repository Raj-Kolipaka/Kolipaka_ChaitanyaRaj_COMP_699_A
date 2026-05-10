import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

from database.models import Expense


class MLService:

    MODEL_PATH = "ml_models/model.pkl"

    # -------- PREPARE DATA --------
    def prepare_data(self, user_id):
        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date).all()

        if len(expenses) < 2:
            return None, None

        amounts = [e.amount for e in expenses]

        X = np.array(range(len(amounts))).reshape(-1, 1)
        y = np.array(amounts)

        return X, y


    # -------- TRAIN MODEL --------
    def train_model(self, user_id):
        X, y = self.prepare_data(user_id)

        if X is None:
            return {"status": False, "message": "Not enough data"}

        model = LinearRegression()
        model.fit(X, y)

        os.makedirs("ml_models", exist_ok=True)

        with open(self.MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        return {"status": True, "message": "Model trained"}


    # -------- LOAD MODEL --------
    def load_model(self):
        if not os.path.exists(self.MODEL_PATH):
            return None

        with open(self.MODEL_PATH, "rb") as f:
            return pickle.load(f)


    # -------- PREDICT NEXT EXPENSE --------
    def predict_next(self, user_id):

        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date).all()

        # 🔹 No data
        if len(expenses) == 0:
            return {"status": True, "predicted_expense": 0}

        amounts = [e.amount for e in expenses]
        avg = sum(amounts) / len(amounts)

        # 🔹 Few records → use average
        if len(expenses) < 2:
            return {
                "status": True,
                "predicted_expense": round(avg, 2)
            }

        # 🔹 Load or train model
        model = self.load_model()
        if not model:
            self.train_model(user_id)
            model = self.load_model()

        if not model:
            return {"status": False, "message": "Model error"}

        n = len(expenses)
        next_index = np.array([[n]])

        try:
            prediction = float(model.predict(next_index)[0])

            # 🔥 Fix unrealistic prediction
            if prediction <= 0:
                prediction = avg

            return {
                "status": True,
                "predicted_expense": round(prediction, 2)
            }

        except:
            return {
                "status": True,
                "predicted_expense": round(avg, 2)
            }


    # -------- GENERATE SUGGESTIONS --------
    def generate_suggestions(self, user_id):

        prediction_data = self.predict_next(user_id)

        if not prediction_data["status"]:
            return ["Not enough data for suggestions"]

        predicted = prediction_data["predicted_expense"]

        expenses = Expense.query.filter_by(user_id=user_id).all()
        total = sum([e.amount for e in expenses])
        avg = total / len(expenses) if expenses else 0

        suggestions = []

        # 🔹 HIGH SPENDING
        if predicted > 30000:
            suggestions.append("Your monthly expenses are high. Try reducing non-essential spending")

        # 🔹 MEDIUM SPENDING
        elif 15000 < predicted <= 30000:
            suggestions.append("Your spending is moderate. Try to optimize food and travel costs")

        # 🔹 LOW SPENDING
        else:
            suggestions.append("Your spending is under control. Maintain this pattern")

        # 🔹 SAVINGS ADVICE
        if predicted > 20000:
            suggestions.append("Set a monthly saving goal of at least ₹2000")
        else:
            suggestions.append("Even small savings of ₹1000 can help in long-term planning")

        # 🔹 TREND ANALYSIS
        if predicted > avg:
            suggestions.append("Your expenses may increase next month. Plan your budget carefully")
        elif predicted < avg:
            suggestions.append("Good job. Your expenses are decreasing compared to past trends")

        # 🔹 LOAN IMPACT
        suggestions.append("Paying small extra EMI can reduce loan duration significantly")

        return suggestions