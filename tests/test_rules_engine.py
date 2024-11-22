import unittest
from rules.rules_engine import evaluate_conditions, apply_actions
from unittest.mock import MagicMock

class TestRulesEngine(unittest.TestCase):

    def setUp(self):
        self.email = {'id': '1', 'from_email': 'example@gmail.com', 'subject': 'Test Email'}
        self.mock_service = MagicMock()
        
        self.rules = [
            {
                "conditions": [
                    {"field": "from", "predicate": "contains", "value": "example@gmail.com"}
                ],
                "actions": ["mark_as_read"]
            }
        ]

    def test_evaluate_conditions(self):
        conditions = self.rules[0]['conditions']
        result = evaluate_conditions(self.email, conditions)
        self.assertTrue(result)  # The condition should match the email

    def test_apply_actions(self):
        actions = self.rules[0]['actions']
        # Mock the actions function
        apply_actions(self.mock_service, self.email, actions)
        
        self.mock_service.users().messages().modify.assert_called_once_with(
            userId='me', 
            id=self.email['id'], 
            body={'removeLabelIds': ['UNREAD']}
        )

if __name__ == '__main__':
    unittest.main()
