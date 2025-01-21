import json
import os

class NotificationHistoryManager:
    """
        Notification history manager static class
    """

    @staticmethod
    def load_data(notification_file):
        """
            Load the notification history data from the file
        """
        try:
            if os.path.exists(notification_file):
                with open(notification_file, 'r') as file:
                    notifications = json.load(file)
                    urgent = notifications.get("urgent", {})
                    upcoming = notifications.get("upcoming", {})
                    high_cost = notifications.get("high_cost", {})

                return (urgent, upcoming, high_cost)

        except Exception as e:
            print(f"Error loading old notifications: {e}")

        return ({}, {}, {})

    @staticmethod
    def save_data(urgent, upcoming, high_cost, notification_file):
        """
            Save the notification history data to the file
        """
        try:
            with open(notification_file, 'w') as file:
                notifications = {
                    "urgent": urgent,
                    "upcoming": upcoming,
                    "high_cost": high_cost
                }
                json.dump(notifications, file)

        except Exception as e:
            print(f"Error saving notifications: {e}")