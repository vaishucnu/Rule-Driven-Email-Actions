import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from rules.email_actions import mark_as_read, mark_as_unread, move_to_folder
from your_module import process_emails, load_rules, evaluate_conditions, apply_actions  # replace 'your_module' with actual module name

class TestEmailProcessing(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        
        self.sample_email = {
            "id": "12345",
            "from_email": "test@example.com",
            "subject": "Urgent: Need Help",
            "body": "This is an urgent email",
            "received_date": "2024-11-23 12:00:00"
        }
        
        self.sample_rules = [
            {
                "conditions": [
                    {"field": "subject", "predicate": "contains", "value": "Urgent"},
                    {"field": "received_date", "predicate": "less than days", "value": "7"}
                ],
                "actions": ["mark_as_read", "move_to_folder:Urgent"],
                "predicate": "All"
            },
            {
                "conditions": [
                    {"field": "from_email", "predicate": "equals", "value": "support@example.com"}
                ],
                "actions": ["mark_as_unread"],
                "predicate": "All"
            }
        ]
        
        load_rules = MagicMock(return_value=self.sample_rules)

    def test_evaluate_conditions_true(self):
        rule = self.sample_rules[0]  # "Urgent" in subject and received within last 7 days
        result = evaluate_conditions(self.sample_email, rule['conditions'], rule_predicate="All")
        self.assertTrue(result)

    def test_evaluate_conditions_false(self):
        modified_email = self.sample_email.copy()
        modified_email["received_date"] = "2020-01-01 12:00:00"  # An old date
        rule = self.sample_rules[0]  # "Urgent" in subject and received within last 7 days
        result = evaluate_conditions(modified_email, rule['conditions'], rule_predicate="All")
        self.assertFalse(result)

    def test_apply_actions_mark_as_read(self):
        apply_actions(self.mock_service, self.sample_email, ["mark_as_read"])
        mark_as_read.assert_called_once_with(self.mock_service, self.sample_email['id'])

    def test_apply_actions_move_to_folder(self):
        apply_actions(self.mock_service, self.sample_email, ["move_to_folder:Urgent"])
        move_to_folder.assert_called_once_with(self.mock_service, self.sample_email['id'], "Urgent")

    def test_process_emails(self):
        process_emails(self.mock_service, [self.sample_email])
        
        mark_as_read.assert_called_once_with(self.mock_service, self.sample_email['id'])
        move_to_folder.assert_called_once_with(self.mock_service, self.sample_email['id'], "Urgent")

    def test_load_rules(self):
        rules = load_rules()
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0]['actions'], ["mark_as_read", "move_to_folder:Urgent"])

if __name__ == "__main__":
    unittest.main()
