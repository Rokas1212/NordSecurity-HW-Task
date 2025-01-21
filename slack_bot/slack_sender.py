from slack_sdk import WebClient
class SlackSender:
    """
        Slack sender class
    """
    def __init__(self, channel, slack_token):
        """
            channel: Channel to send messages to
            slack_token: Slack API token
        """
        self.channel = channel
        self.client = WebClient(token=slack_token)
