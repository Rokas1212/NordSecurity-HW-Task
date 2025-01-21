import unittest
import os
from slack_bot.notification_history_manager import NotificationHistoryManager as NHM


class TestNotificationHistoryManager(unittest.TestCase):

    def setUp(self):
        """
            Initialize the notification history file and dictionaries
        """
        self.notification_file = "test_notification_history.json"
        self.urgent = {"org1": [["nord", "john", 30000, "2025-12-12"]]}
        self.upcoming = {}
        self.high_cost = {}

    def tearDown(self):
        """
            Remove the notification history file after each test
        """
        if os.path.exists(self.notification_file):
            os.remove(self.notification_file)

    def test_save_and_load_data(self):
        """
            Test saving and loading notification history data
        """
        NHM.save_data(self.urgent, self.upcoming, self.high_cost, self.notification_file)
        loaded_urgent, loaded_upcoming, loaded_high_cost = NHM.load_data(self.notification_file)
        self.assertEqual(loaded_urgent, self.urgent)
        self.assertEqual(loaded_upcoming, self.upcoming)
        self.assertEqual(loaded_high_cost, self.high_cost)