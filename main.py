import json
import os
from db_handlers.sqlite_handler import SqliteHandler
from slack_bot.slack_sender import SlackSender
from slack_bot.notification_service import NotificationService as NS
from slack_bot.message_formatting import MessageFormatting as MF
from slack_bot.notification_history_manager import NotificationHistoryManager as NHM
from filters import filter_urgent, filter_upcoming, filter_high_cost
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BOT_CHANNEL = "contracts-bot"
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DATABASE = os.path.join(os.path.dirname(__file__), "contracts.sqlite")
NOTIFICATION_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "notification_history.json")
TABLE_SCHEMAS_FILE = os.path.join(os.path.dirname(__file__), "table_schemas.json")
# Load the notification history data
URGENT, UPCOMING, HIGH_COST = NHM.load_data(NOTIFICATION_HISTORY_FILE)

def initialize_dictionaries(table_schemas, urgent, upcoming, high_cost):
    """
    Initialize dictionaries for each table
    """
    for table in table_schemas.keys():
        if table not in urgent:
            urgent[table] = []
        if table not in upcoming:
            upcoming[table] = []
        if table not in high_cost:
            high_cost[table] = []

def main():
    try:
        # Initialize message
        message = datetime.now().strftime("%d/%m/%Y") + "\n" +  "-" * 30

        # Create a SlackSender object
        sender = SlackSender(BOT_CHANNEL, SLACK_TOKEN)

        # Connect to the SQLite database
        db = SqliteHandler(DATABASE)

        # Read table schemas file
        with open(TABLE_SCHEMAS_FILE, 'r') as file:
            table_schemas = json.load(file)

        # Initialize dictionaries for each table (organization)
        initialize_dictionaries(table_schemas, URGENT, UPCOMING, HIGH_COST)

        # Iterate through each table and format contract data into a message
        for table, columns in table_schemas.items():
            rows = db.fetch_all_table_rows(table, columns)
            urgent = filter_urgent(rows, columns)
            upcoming = filter_upcoming(rows, columns)
            high_cost = filter_high_cost(rows, columns)

            # Prepare the message
            message += MF.prepare_contract_message(URGENT, "URGENT", table, urgent, columns)
            message += MF.prepare_contract_message(UPCOMING, "UPCOMING", table, upcoming, columns)
            message += MF.prepare_contract_message(HIGH_COST, "HIGH-COST", table, high_cost, columns)

            # Store the filtered contracts
            URGENT[table] = urgent
            UPCOMING[table] = upcoming
            HIGH_COST[table] = high_cost

        # Send the message to the Slack channel
        NS.send_message(message, sender)
        
        #Save the notification history data
        NHM.save_data(URGENT, UPCOMING, HIGH_COST, NOTIFICATION_HISTORY_FILE)

        db.close_connection()
    except Exception as e:
        with open('errors.log', 'a') as log_file:
            log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [Main] Script ran into an error: {e}\n")

if __name__ == "__main__":
    main()