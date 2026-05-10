from models.user import User

class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, "admin")

    def view_reports(self, report_service):
        return report_service.generate_system_report()

    def manage_templates(self, planner_service, data):
        return planner_service.update_templates(data)