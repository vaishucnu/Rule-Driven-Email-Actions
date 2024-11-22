import sqlite3

def create_connection():
    conn = sqlite3.connect('emails.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            from_address TEXT,
            to_address TEXT,
            subject TEXT,
            body TEXT,
            received_date TEXT,
            label_ids TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_email(email):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO emails (id, from_address, to_address, subject, body, received_date, label_ids)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (email['id'], email['from'], email['to'], email['subject'], email['body'], email['received_date'], email['label_ids']))
    conn.commit()
    conn.close()

def store_emails_in_db(emails):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            from_email TEXT,
            subject TEXT,
            received_date TEXT,
            body TEXT
        )
    """)

    for email in emails:
        cursor.execute("""
            INSERT OR IGNORE INTO emails (id, from_email, subject, received_date, body)
            VALUES (?, ?, ?, ?, ?)
        """, (email["id"], email["from"], email["subject"], email["received_date"], email["body"]))

    conn.commit()
    conn.close()

def fetch_all_email():
    conn = create_connection()
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
