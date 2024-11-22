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
        "contains": lambda field, value: value in field,
        "does not contain": lambda field, value: value not in field,
        "greater than": lambda field, value: field > value,
        "less than": lambda field, value: field < value
    }

    results = []
    for condition in conditions:
        field_value = email.get(condition['field'], "")
        predicate = condition['predicate']
        value = condition['value']

        if predicate in operators:
            results.append(operators[predicate](field_value, value))
        else:
            print(f"Unsupported predicate: {predicate}")

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
