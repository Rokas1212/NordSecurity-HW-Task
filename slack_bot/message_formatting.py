
class MessageFormatting:
    """
        Class to format messages for the Slack bot
    """

    @staticmethod
    def check_duplicates(contract_type, table, contract):
        """
            Check if the team was already notified about the contract to avoid duplicates
            contract_type: Type of contract
            table: Database table name also representing the organization name
            contract: Contract details
            returns: True if the contract exists, False otherwise
        """
        return list(contract) in contract_type.get(table, [])

    @staticmethod
    def format_contract(contract, columns):
        """
            Format the contract details into a snippet for the message
            contract: Contract details
            columns: Dictionary of column mappings
            returns: Formatted snippet
        """
        try:
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
            print(f"Error formatting contract: {e}")
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
        message = f"\n```*{contract_type.upper()} {table.upper()} CONTRACTS*\n"
        for contract in contracts:
            if MessageFormatting.check_duplicates(notification_history, table, contract):
                continue
            message += MessageFormatting.format_contract(contract, columns)
        if message[-2] == "*":
            message += f"No expiring {contract_type.lower()} contracts found"
        message += "```"
        return message