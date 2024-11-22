from googleapiclient.errors import HttpError

def modify_email_labels(service, email_id, body):
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body=body
        ).execute()
        
        print(f"Email {email_id} modified successfully.")
    except HttpError as error:
        print(f"Error modifying email {email_id}: {error}")


def mark_as_read(service, email_id):
    body = {'removeLabelIds': ['UNREAD']}
    modify_email_labels(service, email_id, body)
    print(f"marked as read: {email_id}")


def mark_as_unread(service, email_id):
    body = {'addLabelIds': ['UNREAD']}
    modify_email_labels(service, email_id, body)
    print(f"marked as unread: {email_id}")


def move_to_folder(service, email_id, folder_label):
    existing_labels = get_labels(service)

    if folder_label not in existing_labels:
        print(f"Label '{folder_label}' does not exist. Creating it now...")
        folder_label_id = create_label(service, folder_label)
    else:
        folder_label_id = existing_labels[folder_label]

    body = {'addLabelIds': [folder_label_id]}
    modify_email_labels(service, email_id, body)
    print(f"Moved to foler {email_id}: {folder_label_id}")

def get_labels(service):
    try:
        labels_response = service.users().labels().list(userId='me').execute()
        labels = labels_response.get('labels', [])
        label_map = {label['name']: label['id'] for label in labels}
        return label_map
    except HttpError as error:
        print(f"Error fetching labels: {error}")
        return {}

def create_label(service, label_name):
    label_object = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    try:
        created_label = service.users().labels().create(userId='me', body=label_object).execute()
        print(f"Label '{label_name}' created.")
        return created_label['id']
    except HttpError as error:
        print(f"Error creating label '{label_name}': {error}")
        return None
