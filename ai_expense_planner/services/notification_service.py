from database.models import Notification, Loan
from database.db import db
from datetime import datetime, timedelta


class NotificationService:

    def create_notification(self, user_id, message):
        notification = Notification(
            user_id=user_id,
            message=message,
            date=datetime.utcnow(),
            is_read=False
        )

        db.session.add(notification)
        db.session.commit()

        return {"status": True, "message": "Notification created"}


    def get_notifications(self, user_id):
        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.date.desc()).all()

        data = []
        for n in notifications:
            data.append({
                "id": n.id,
                "message": n.message,
                "date": n.date,
                "is_read": n.is_read
            })

        return data


    def mark_as_read(self, notification_id):
        notification = Notification.query.get(notification_id)

        if not notification:
            return {"status": False}

        notification.is_read = True
        db.session.commit()

        return {"status": True}


    def check_emi_reminder(self, user_id):
        loan = Loan.query.filter_by(user_id=user_id).first()

        if not loan:
            return

        # simple reminder logic: every 30 days
        last_date = loan.start_date
        next_due = last_date + timedelta(days=30)

        today = datetime.utcnow()

        if today >= next_due:
            message = "EMI due soon. Please make your payment."

            existing = Notification.query.filter_by(user_id=user_id, message=message).first()

            if not existing:
                self.create_notification(user_id, message)