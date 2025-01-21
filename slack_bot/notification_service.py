from slack_sdk.errors import SlackApiError
from datetime import datetime

class NotificationService:
    """
        Notification service static class to send messages to Slack
    """
    @staticmethod
    def send_message(message, sender):
        """
            Send a message to a Slack channel
            message: Message to send
            sender: SlackSender object
        """
        try:
            response = sender.client.chat_postMessage(
                channel=sender.channel,
                text=message
            )
            return response.get("ok")
        except SlackApiError as e:
            with open('errors.log', 'a') as log_file:
                log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [Notification Service] Error sending message: {e}\n")