import unittest
from email_api.email_api import mark_as_read, mark_as_unread, move_to_folder
from unittest.mock import MagicMock

class TestEmailApi(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        self.email_id = '12345'
        self.folder_label = 'Assignments'

    def test_mark_as_read(self):
        mark_as_read(self.mock_service, self.email_id)
        
        self.mock_service.users().messages().modify.assert_called_once_with(
            userId='me', 
            id=self.email_id, 
            body={'removeLabelIds': ['UNREAD']}
        )

    def test_mark_as_unread(self):
        mark_as_unread(self.mock_service, self.email_id)
        
        self.mock_service.users().messages().modify.assert_called_once_with(
            userId='me', 
            id=self.email_id, 
            body={'addLabelIds': ['UNREAD']}
        )

    def test_move_to_folder(self):
        move_to_folder(self.mock_service, self.email_id, self.folder_label)
        
        self.mock_service.users().messages().modify.assert_called_once_with(
            userId='me', 
            id=self.email_id, 
            body={'addLabelIds': [self.folder_label]}
        )

if __name__ == '__main__':
    unittest.main()
