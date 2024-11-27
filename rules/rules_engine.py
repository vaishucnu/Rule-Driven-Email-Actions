import json
from datetime import datetime
from rules.email_actions import mark_as_read, mark_as_unread, move_to_folder

# Load rules from JSON file
def load_rules():
    file_path = 'rules/rules.json'
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Rules file not found: {file_path}")
        return []

def evaluate_conditions(email, conditions, rule_predicate="All"):
    operators = {
        # String-based predicates
        "contains": lambda field, value: value in field,
        "does not contain": lambda field, value: value not in field,
        "equals": lambda field, value: field == value,
        "does not equal": lambda field, value: field != value,
        # Date-based predicates
        "less than days": lambda field, value: (datetime.now() - datetime.strptime(field, "%Y-%m-%d")).days < int(value),
        "greater than days": lambda field, value: (datetime.now() - datetime.strptime(field, "%Y-%m-%d")).days > int(value),
        "less than months": lambda field, value: (datetime.now() - datetime.strptime(field, "%Y-%m-%d")).days / 30 < int(value),
        "greater than months": lambda field, value: (datetime.now() - datetime.strptime(field, "%Y-%m-%d")).days / 30 > int(value)
    }

    results = []
    for condition in conditions:
        field_name = condition['field']
        predicate = condition['predicate']
        value = condition['value']

        field_value = email.get(field_name, "")

        # Handle missing fields
        if not field_value:
            print(f"Warning: Field '{field_name}' not found in email.")
            results.append(False)
            continue

        if predicate in operators:
            try:
                results.append(operators[predicate](field_value, value))
            except Exception as e:
                print(f"Error evaluating condition: {condition}. Error: {e}")
                results.append(False)
        else:
            print(f"Unsupported predicate: {predicate}")
            results.append(False)

    return all(results) if rule_predicate == "All" else any(results)


def apply_actions(service, email, actions):
    for action in actions:
        if action == "mark_as_read":
            mark_as_read(service, email['id'])
        elif action == "mark_as_unread":
            mark_as_unread(service, email['id'])
        elif action.startswith("move_to_folder:"):
            folder_label = action.split(":")[1]
            move_to_folder(service, email['id'], folder_label)
        else:
            print(f"Unsupported action: {action}")

def process_emails(service, emails):
    rules = load_rules()
    
    for rule in rules:
        rule_predicate = rule.get('predicate', 'All')  # Default to "All"
        for email in emails:
            if evaluate_conditions(email, rule['conditions'], rule_predicate):
                apply_actions(service, email, rule['actions'])
