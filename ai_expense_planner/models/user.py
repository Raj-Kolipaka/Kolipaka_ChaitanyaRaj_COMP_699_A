class User:
    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def get_role(self):
        return self.role

    def get_details(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }