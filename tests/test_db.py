import unittest
import sqlite3
from database.db import fetch_all_email, insert_email  # Assuming these functions are in db.py
from unittest.mock import patch

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")  # Use in-memory DB for testing
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE emails (
                                id TEXT PRIMARY KEY,
                                from_email TEXT NOT NULL,
                                subject TEXT,
                                body TEXT,
                                received_date DATETIME,
                                status BOOLEAN NOT NULL DEFAULT 0
                            )''')
        self.conn.commit()

    def test_insert_email(self):
        email = {
            'id': '1',
            'from_email': 'example@gmail.com',
            'subject': 'Test Email',
            'received_date': '2024-11-22',
            'body': 'Test body',
            'status': 0
        }
        insert_email(self.conn, email)
        
        self.cursor.execute("SELECT * FROM emails WHERE id = '1'")
        row = self.cursor.fetchone()
        
        self.assertEqual(row[0], '1')  # Check email ID
        self.assertEqual(row[1], 'example@gmail.com')  # Check from_email

    def test_fetch_all_email(self):
        email = {
            'id': '1',
            'from_email': 'example@gmail.com',
            'subject': 'Test Email',
            'received_date': '2024-11-22',
            'body': 'Test body',
            'status': 0
        }
        insert_email(self.conn, email)
        
        emails = fetch_all_email(self.conn)
        self.assertEqual(len(emails), 1)  # Check if one email is fetched
        self.assertEqual(emails[0]['id'], '1')  # Check if fetched email ID matches

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
