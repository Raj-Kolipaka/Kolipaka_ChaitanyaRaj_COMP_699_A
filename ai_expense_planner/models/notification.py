class Notification:
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def send(self):
        return f"Notification sent to user {self.user_id}: {self.message}"