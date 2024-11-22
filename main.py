from email_api.email_api import authenticate_gmail, fetch_emails
from database.db import create_table, insert_email, fetch_all_email, store_emails_in_db
from rules.rules_engine import process_emails

def main():
    service = authenticate_gmail()
    emails = fetch_emails(service)
    store_emails_in_db(emails)
    emails_in_db = fetch_all_email()
    process_emails(service, emails_in_db)

if __name__ == "__main__":
    main()
