# Email Processing Rules Engine

Email Processing Rules Engine is a Python-based application that interacts with the Gmail API to automatically process the emails. Users can define rules to evaluate specific conditions (such as sender, subject, etc.), and the application will perform actions like marking emails as read, moving them to folders, and more.

## Features

- Fetches unread emails from Gmail using the Gmail API.
- Evaluates emails based on user-defined conditions (e.g., from email address, subject).
- Applies actions based on the conditions (e.g., mark as read, move to folder).
- Easy configuration via JSON-based rules and Gmail API credentials.

## Installation

1. Clone the repository:
	```bash
   git clone https://github.com/yourusername/email-processing.git
   cd email-processing
   ```

2. Install the required dependencies:

	```bash
	 python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
	```

3. Set up your Gmail API credentials:

	Go to the Google Developer Console.
	Create a new project and enable the Gmail API.
	Download the credentials JSON file and place it in the config/ directory as config.json.

## Configuration

## Gmail API Configuration
	Add your Gmail API credentials to config/config.json. Ensure the credentials have the correct permissions (https://www.googleapis.com/auth/gmail.modify).

## Defining Rules
	Define email processing rules in rules/rules.json

## Usage
	1. Run the main script to start processing emails:
		```bash
			python main.py
		```

	2. The script will:

		Fetch unread emails from your Gmail inbox.
		Apply the defined rules to the emails (e.g., mark as read or move to a folder).
		Print logs of actions performed.

## Directory Structure

email-processing/
├── config/                     # Configuration files
│   └── config.json             # Gmail API credentials and settings
├── database/                   # Database operations
│   └── db.py                   # Database functions to interact with email records
├── email_api/                  # Gmail API integration
│   └── email_api.py            # Functions to interact with Gmail API
├── rules/                      # Email rules and engine
│   └── rules.json              # Email processing rules
│   └── rules_engine.py         # Logic for evaluating and applying rules
├── tests/                      # Unit tests
│   └── test_email_api.py       # Tests for Gmail API interactions
│   └── test_rules_engine.py    # Tests for rule evaluation and actions
│   └── test_db.py              # Tests for database operations
├── main.py                     # Main script to run the email processing engine
├── requirements.txt            # Dependencies for the project
└── README.md                   # Project documentation


Tests
Run tests:

Ensure you have pytest installed:

pip install pytest
Run all tests:

pytest
Test coverage:

The tests cover key components of the project, including Gmail API interactions, rule evaluations, and database operations.