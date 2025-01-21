import unittest
from slack_bot.notification_service import NotificationService
from slack_bot.slack_sender import SlackSender
from dotenv import load_dotenv
import os

class TestNotificationService(unittest.TestCase):

    def setUp(self):
        """
            Initialize the SlackSender object
        """
        load_dotenv()
        token = os.getenv("SLACK_BOT_TOKEN")
        self.sender = SlackSender("contracts-bot", token)

    def test_send_message_success(self):
        """
            Test sending a message to a Slack channel
        """
        response = NotificationService.send_message("TESTING CONNECTIVITY", self.sender)
        self.assertTrue(response)
    
    def test_send_message_failure(self):
        """
            Test sending a message to a Slack channel with an invalid token
        """
        response = NotificationService.send_message("TESTING CONNECTIVITY", SlackSender("contracts-bot", "invalid_token"))
        self.assertFalse(response)