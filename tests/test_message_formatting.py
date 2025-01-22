import unittest
from helpers.message_formatting import MessageFormatting as MF

class TestMessageFormatting(unittest.TestCase):
    def setUp(self):
        self.columns = {
            "software": "name",
            "owner": "owner",
            "annual_cost": "annual_cost",
            "contract_expiration": "contract_expiration"
        }
        self.contract = ("Tool", "John McJohnny", 10000, "2025-01-10")
        self.table = "Wizards Inc"
        self.notification_history = {
                self.table: [list(self.contract)]
        }


    def test_check_duplicates_positive(self):
        """
        Test that the check_duplicates method correctly identifies contracts that the team was already notified about.
        """
        self.assertTrue(MF.check_duplicates(self.notification_history, self.table, self.contract))

    def test_check_duplicates_negative(self):
        """
        Test that the check_duplicates method correctly identifies contracts that the team was not notified about.
        """
        self.assertFalse(MF.check_duplicates(self.notification_history, self.table, ("Tool", "John McJohnny", 20000, "2025-01-10")))

    def test_format_contract(self):
        """
        Test that the format_contract method correctly formats the contract details.
        """
        expected = """
        * Software/Tool: Tool
        * Owner:         John McJohnny
        * Annual Cost:   $10000
        * Expiration:    2025-01-10
        """
        self.assertEqual(MF.format_contract(self.contract, self.columns), expected)
    
    def test_format_contract_exception(self):
        """
        Test that the format_contract method correctly handles exceptions and returns an empty string.
        """
        self.columns = {}
        self.assertEqual(MF.format_contract(self.contract, self.columns), "")
    
    def test_prepare_contract_message_no_contracts(self):
        """
        Test that the prepare_contract_message method correctly handles the case when there are no contracts.
        """
        contracts = []
        expected = f"\n```*{"URGENT"} {self.table.upper()} CONTRACTS*\nNo expiring urgent contracts found```"
        self.assertEqual(MF.prepare_contract_message(self.notification_history, "URGENT", self.table, contracts, self.columns), expected)

    def test_prepare_contract_message_with_contracts(self):
        """
        Test that the prepare_contract_message method correctly prepares the message when there are contracts.
        """
        contracts = [self.contract]
        expected = f"\n```*{"URGENT"} {self.table.upper()} CONTRACTS*\n{MF.format_contract(self.contract, self.columns)}```"
        self.assertEqual(MF.prepare_contract_message({}, "URGENT", self.table, contracts, self.columns), expected)
    
    def test_prepare_contract_message_duplicates(self):
        """
        Test that the prepare_contract_message method correctly skips contracts that were already notified about.
        """
        contracts = [self.contract]
        expected = f"\n```*{"URGENT"} {self.table.upper()} CONTRACTS*\nNo expiring urgent contracts found```"
        self.assertEqual(MF.prepare_contract_message(self.notification_history, "URGENT", self.table, contracts, self.columns), expected)