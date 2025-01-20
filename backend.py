import csv

DB_FILE = "./catalog.csv"

# Read data from the database
def read_catalog():
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

# Write data back to the database
def save_catalog(catalog):
    with open(DB_FILE, mode='w', newline='\n') as file:
        fieldnames = ["ID", "Name", "Description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog)

# Validate input data
def validate_item(item):
    return item.get("ID") and item.get("Name") and item.get("Description")

# Add a new item
def add_item(catalog, new_item):
    if validate_item(new_item):
        catalog.append(new_item)
        return True
    return False

# Edit an existing item
def edit_item(catalog, item_id, updates):
    for item in catalog:
        if item["ID"] == item_id:
            item.update(updates)
            return True
    return False
