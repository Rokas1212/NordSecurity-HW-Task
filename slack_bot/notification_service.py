from slack_sdk.errors import SlackApiError

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
            print(response)
        except SlackApiError as e:
            error_message = e.response.get("error", "Unknown error")
            print(f"Error sending message: {error_message}")