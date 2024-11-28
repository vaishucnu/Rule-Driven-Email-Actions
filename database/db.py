import sqlite3

def create_connection():
    conn = sqlite3.connect('emails.db')
    return conn

def store_emails_in_db(emails):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            from_email TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            received_date DATETIME,
            status BOOLEAN NOT NULL DEFAULT 0 -- 0 for unread, 1 for read
        )
    """)

    for email in emails:
        cursor.execute("""
            INSERT OR IGNORE INTO emails (id, from_email, subject, body, received_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email["id"], email["from"], email["subject"], email["body"], email["received_date"], email["status"]))

    conn.commit()
    conn.close()

def fetch_all_email():
    conn = create_connection()
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    cursor.execute("PRAGMA table_info(emails);")
    columns = cursor.fetchall()
    for column in columns:
        print(dict(column))
    conn.close()
    return [dict(row) for row in rows]