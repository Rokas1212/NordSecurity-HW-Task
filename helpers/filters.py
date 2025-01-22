from datetime import datetime, timedelta

# Constants for column names used in filtering
ANNUAL_COST = "annual_cost"
CONTRACT_EXPIRATION = "contract_expiration"

def filter_urgent(rows, columns):
    """
        Filter contracts that are due in the next 3 days
        rows: List of contracts
        columns: Dictionary of column mappings
        returns: List of urgent contracts
    """
    expiration_index = list(columns.keys()).index(CONTRACT_EXPIRATION)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return [
        row for row in rows if today <= datetime.strptime(row[expiration_index], '%Y-%m-%d') <= today + timedelta(days=3)
    ]

def filter_upcoming(rows, columns):
    """
        Filter contracts that are due in the next 14 days and are not urgent (due in the next 3 days)
        rows: List of contracts
        returns: List of upcoming contracts
    """
    expiration_index = list(columns.keys()).index(CONTRACT_EXPIRATION)
    return [row for row in rows if datetime.strptime(row[expiration_index], '%Y-%m-%d') > datetime.now() + timedelta(days=3) 
                                and datetime.strptime(row[expiration_index], '%Y-%m-%d') <= datetime.now() + timedelta(days=14)]

def filter_high_cost(rows, columns):
    """
        Filter contracts that have a contract value greater than 10000, are due within next 30 days and are not "URGENT" or "UPCOMING"
        rows: List of contracts
        columns: Dictionary of column mappings
        returns: List of high cost contracts
    """
    cost_index = list(columns.keys()).index(ANNUAL_COST)
    expiration_index = list(columns.keys()).index(CONTRACT_EXPIRATION)
    return [row for row in rows if row[cost_index] >= 10000 
                                and datetime.strptime(row[expiration_index], '%Y-%m-%d') > datetime.now() + timedelta(days=14)
                                and datetime.strptime(row[expiration_index], '%Y-%m-%d') <= datetime.now() + timedelta(days=30)]