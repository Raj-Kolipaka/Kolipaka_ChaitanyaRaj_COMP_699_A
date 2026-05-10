from models.user import User

class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "student")

    def add_expense(self, expense_service, data):
        return expense_service.add_expense(self.user_id, data)

    def request_analysis(self, ml_service):
        return ml_service.analyze(self.user_id)

    def generate_plan(self, planner_service):
        return planner_service.generate_plan(self.user_id)