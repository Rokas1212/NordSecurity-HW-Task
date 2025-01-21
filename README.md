# Nord Security Junior Python Engineer HW Task

## User Guide
- Add the Slack APP to your Slack channel, name the channel contracts-bot
- Describe table schemas in table_schemas.json located in the root directory
- Create a .env file in the root directory of the project and assign your API key to SLACK_BOT_TOKEN
- Run main.py
- All contracts that were sent out as notifications shall appear in the notifications_history.json file
- These notifications will not be sent out the next time the script is ran

## Automating execution
- To automate the script to run once per day run script.sh (time can be edited in the shell script)
- Alternatively a cronjob can be setup it would look something like this:
  - 0 8 * * * python3 path/to/main.py
  - The cronjob above would run the script once every day at 8

## Project Guide
- db_handles contains the SQLiteHandler, which is responsible for interacting with the database
- slack_bot contains:
  - message_formatting - static class used for formatting the slack messages
  - notificaton_history_manager - static class used to track contracts that have been sent out through notifications (since the provided DB tables did not have primary keys I used a json file)
  - notification_service - static class that abstracts the sending of a message in slack and takes the client (sender) object as input
  - slack_sender - sender class that allows to create a sender object
- tests directory contains unit tests
- project root contains:
    - main.py - responsible for executing the script
    - filters.py - responsible for filtering contracts by type

## Running Unit Tests
- Navigate to the root directory
- Run this command: ```python -m unittest discover tests```

## Dependencies
- Needed pip modules are outlined in requirements.txt