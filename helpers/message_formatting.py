
from datetime import datetime

class MessageFormatting:
    """
        Class to format messages for the Slack bot
    """

    @staticmethod
    def check_duplicates(notification_history, table, contract):
        """
            Check if the team was already notified about the contract to avoid duplicates
            notification_history: Dictionary of notification history
            table: Database table name also representing the organization name
            contract: Contract details
            returns: True if the contract exists, False otherwise
        """
        return list(contract) in notification_history.get(table, [])

    @staticmethod
    def format_contract(contract, columns):
        """
            Format the contract details into a snippet for the message
            contract: Contract details
            columns: Dictionary of column mappings
            returns: Formatted snippet
        """
        try:
            if not columns:
                raise Exception("Columns dictionary is empty")
            # Get the index of each column
            software_index = list(columns.keys()).index("software")
            owner_index = list(columns.keys()).index("owner")
            annual_cost_index = list(columns.keys()).index("annual_cost")
            expiration_index = list(columns.keys()).index("contract_expiration")
            return f"""
        * Software/Tool: {contract[software_index]}
        * Owner:         {contract[owner_index]}
        * Annual Cost:   ${contract[annual_cost_index]}
        * Expiration:    {contract[expiration_index]}
        """
        except Exception as e:
            with open('errors.log', 'a') as log_file:
                log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [MessageFormatting] Error formatting contract: {e}\n")
            return ""
        
    @staticmethod
    def prepare_contract_message(notification_history, contract_type, table, contracts, columns):
        """
        Prepare the message for a specific contract type
        notification_history: Dictionary of a notification history
        contract_type: Type of contract (URGENT, UPCOMING, HIGH_COST)
        table: Table name, also representing the organization name
        contracts: List of contracts
        columns: Dictionary of column mappings
        returns: Formatted message
        """
        try:
            message = f"\n```*{contract_type.upper()} {table.upper()} CONTRACTS*\n"
            for contract in contracts:
                if MessageFormatting.check_duplicates(notification_history, table, contract):
                    continue
                message += MessageFormatting.format_contract(contract, columns)
            if message[-2] == "*":
                message += f"No expiring {contract_type.lower()} contracts found"
            message += "```"
            return message
        except Exception as e:
            with open('errors.log', 'a') as log_file:
                log_file.write(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] [MessageFormatting] Error preparing contract message: {e}\n")
            return f"An error occurred while preparing the data for {table} contracts"