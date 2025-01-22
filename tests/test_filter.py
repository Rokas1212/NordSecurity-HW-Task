import unittest
from datetime import datetime, timedelta
from helpers.filters import filter_urgent, filter_upcoming, filter_high_cost


class TestFilters(unittest.TestCase):

    def setUp(self):
        """Set up the test data."""
        
        self.column_mappings = {
            "name": "name",
            "contract_expiration": "contract_expiration",
            "annual_cost": "cost"
        }
        self.rows = [
            ("Contract Urgent", (datetime.now() + timedelta(days=0)).strftime('%Y-%m-%d'), 100),
            ("Contract HighCost", (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'), 10000),
            ("Contract Upcoming", (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'), 300),
            ("Contract Expired", (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), 100)
        ]

    def test_filter_urgent(self):
        """
        Test the filter_urgent function.
        """
        urgent_contracts = filter_urgent(self.rows, self.column_mappings)
        self.assertEqual(len(urgent_contracts), 1)
        self.assertEqual(urgent_contracts[0][0], "Contract Urgent")

    def test_filter_upcoming(self):
        """
        Test the filter_upcoming function.
        """
        upcoming_contracts = filter_upcoming(self.rows, self.column_mappings)
        self.assertEqual(len(upcoming_contracts), 1)
        self.assertEqual(upcoming_contracts[0][0], "Contract Upcoming")
    
    def test_filter_high_cost(self):
        """
        Test the filter_high_cost function.
        """
        high_cost_contracts = filter_high_cost(self.rows, self.column_mappings)
        self.assertEqual(len(high_cost_contracts), 1)
        self.assertEqual(high_cost_contracts[0][0], "Contract HighCost")

    def test_empty_rows(self):
        """
        Test the filter functions with an empty list of rows.
        """
        self.assertEqual(filter_urgent([], self.column_mappings), [])
        self.assertEqual(filter_upcoming([], self.column_mappings), [])
        self.assertEqual(filter_high_cost([], self.column_mappings), [])