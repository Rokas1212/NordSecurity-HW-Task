import json
import os
from datetime import datetime

class NotificationHistoryManager:
    """
        Notification history manager static class
    """

    @staticmethod
    def load_data(notification_file):
        """
            Load the contract notification history data from the file
            notification_file: Path to the notification history file
            returns: Tuple of urgent, upcoming, and high cost notifications
        """
        try:
            if os.path.exists(notification_file):
                with open(notification_file, 'r') as file:
                    notifications = json.load(file)
                    # Get the urgent, upcoming, and high cost notifications if they exist, otherwise return empty dictionaries
                    urgent = notifications.get("urgent", {})
                    upcoming = notifications.get("upcoming", {})
                    high_cost = notifications.get("high_cost", {})

                return (urgent, upcoming, high_cost)
        except Exception as e:
            with open('errors.log', 'a') as log_file:
                log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [Notification History Manager] Error loading notifications: {e}\n")

        return ({}, {}, {})

    @staticmethod
    def save_data(urgent, upcoming, high_cost, notification_file):
        """
            Save the sent contract notification history data to a json file
            urgent: Urgent notifications
            upcoming: Upcoming notifications
            high_cost: High cost notifications
            notification_file: Path to the notification history file
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
            with open('errors.log', 'a') as log_file:
                log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [Notification History Manager] Error saving notifications: {e}\n")