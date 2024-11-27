import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

"""Authenticate and build the Gmail API client."""
def authenticate_gmail():
    creds = None
    # Check if token.pickle file exists (previously saved credentials)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/config.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    try:
        # Build the Gmail API client
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

"""Fetch emails from the inbox."""
def fetch_emails(service):
    try:
        #results = service.users().messages().list(userId='me', q="is:unread").execute()
        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])
        emails = []

        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            email_data = {
                "id": message.get("id", ""),
                "from": extract_header(headers, "from"),
                "subject": extract_header(headers, "subject"),
                "received_date": parse_received_date(extract_header(headers, "date")),
                "body": payload['parts'][0]['body']['data']
            }
            emails.append(email_data)
        return emails
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def parse_received_date(raw_date):
    try:
        return datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")
    except (ValueError, TypeError) as e:
        print(f"Error parsing date: {raw_date}. Error: {e}")
        return ""

def extract_header(headers, name):
    return next((header["value"] for header in headers if header["name"].lower() == name.lower()), "")
