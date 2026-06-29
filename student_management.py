
import csv
import json
import os
import logging
import re

logging.basicConfig(
    filename='student_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CSV_FILE = 'students.csv'
JSON_FILE = 'students.json'

class StudentNotFoundError(Exception):
    def __init__(self, reg_no, message="Student record not found in the system."):
        self.reg_no = reg_no
        self.message = f"{message} (Reg No: {reg_no})"
        super().__init__(self.message)

def initialize_files():
    try:
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Registration Number', 'Name'])
        
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, mode='w', encoding='utf-8') as f:
                json.dump({}, f)
    except Exception as e:
        logging.critical(f"Failed to initialize storage files: {e}")
        print(f"Critical Error: System could not initialize storage. {e}")
        exit(1)

def validate_reg_no(reg_no):
    pattern = r'^[A-Za-z0-9\/]+$'
    return bool(re.match(pattern, reg_no))

def load_csv_records():
    records = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def save_csv_records(records):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['Registration Number', 'Name']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def load_json_records():
    with open(JSON_FILE, mode='r', encoding='utf-8') as f:
        return json.load(f)

def save_json_records(data):
    with open(JSON_FILE, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def add_student():
    print("\n--- Add New Student ---")
    try:
        reg_no = input("Enter Registration Number: ").strip()
        if not reg_no or not validate_reg_no(reg_no):
            print("Invalid format. Alphanumeric and '/' characters only.")
            return

        csv_records = load_csv_records()
        if any(row['Registration Number'].lower() == reg_no.lower() for row in csv_records):
            print(f"Error: Student with Reg No '{reg_no}' already exists.")
            logging.warning(f"Failed add attempt: Duplicate Reg No '{reg_no}'")
            return

        name = input("Enter Student Full Name: ").strip()
        if not name:
            print("Name field cannot be empty.")
            return

        address = input("Enter Address: ").strip()
        contact = input("Enter Contact/Phone Number: ").strip()
        program = input("Enter Academic Program: ").strip()

        csv_records.append({'Registration Number': reg_no, 'Name': name})
        save_csv_records(csv_records)

        json_data = load_json_records()
        json_data[reg_no] = {
            'address': address,
            'contact': contact,
            'program': program
        }
        save_json_records(json_data)

        print(f"Success: Student {name} registered successfully!")
        logging.info(f"Successfully added student: {reg_no} - {name}")

    except Exception as e:
        logging.error(f"Error occurred while adding student: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Add operation process finalized.")

def view_all_students():

    print("\n--- All Student Records ---")
    try:
        csv_records = load_csv_records()
        json_data = load_json_records()

        if not csv_records:
            print("No student records found.")
            return

        print(f"{'Reg No':<15} | {'Name':<20} | {'Program':<15} | {'Contact':<15} | {'Address':<20}")
        print("-" * 90)
        
        for row in csv_records:
            r_no = row['Registration Number']
            name = row['Name']
            meta = json_data.get(r_no, {'program': 'N/A', 'contact': 'N/A', 'address': 'N/A'})
            
            print(f"{r_no:<15} | {name:<20} | {meta['program']:<15} | {meta['contact']:<15} | {meta['address']:<20}")
        
        logging.info("Viewed all student records.")
    except Exception as e:
        logging.error(f"Error viewing student records: {e}")
        print("Could not retrieve student list.")

def search_student():
    print("\n--- Search Student ---")
    try:
        reg_no = input("Enter Registration Number to search: ").strip()
        csv_records = load_csv_records()
        
        # Look up match
        match = next((row for row in csv_records if row['Registration Number'].lower() == reg_no.lower()), None)
        
        if not match:
            raise StudentNotFoundError(reg_no)
        
        # If found, match actual key casing from CSV
        actual_reg_no = match['Registration Number']
        json_data = load_json_records()
        meta = json_data.get(actual_reg_no, {'program': 'N/A', 'contact': 'N/A', 'address': 'N/A'})

        print("\nRecord Found:")
        print(f"Registration No : {actual_reg_no}")
        print(f"Name            : {match['Name']}")
        print(f"Program         : {meta['program']}")
        print(f"Contact         : {meta['contact']}")
        print(f"Address         : {meta['address']}")
        
        logging.info(f"Successful search for Reg No: {actual_reg_no}")

    except StudentNotFoundError as snfe:
        print(f"Search Failed: {snfe.message}")
        logging.warning(f"Search attempt failed: {snfe.message}")
    except Exception as e:
        logging.error(f"Unexpected error during search: {e}")
        print("An error occurred during search selection.")

def update_student():
    print("\n--- Update Student Details ---")
    try:
        reg_no = input("Enter Registration Number to update: ").strip()
        csv_records = load_csv_records()
        
        match = next((row for row in csv_records if row['Registration Number'].lower() == reg_no.lower()), None)
        if not match:
            raise StudentNotFoundError(reg_no)

        actual_reg_no = match['Registration Number']
        json_data = load_json_records()
        meta = json_data.get(actual_reg_no, {'program': '', 'contact': '', 'address': ''})

        print(f"Updating record for {match['Name']} ({actual_reg_no}). Leave blank to keep current value.")
        
        new_name = input(f"New Name [{match['Name']}]: ").strip()
        new_program = input(f"New Program [{meta.get('program', 'N/A')}]: ").strip()
        new_contact = input(f"New Contact [{meta.get('contact', 'N/A')}]: ").strip()
        new_address = input(f"New Address [{meta.get('address', 'N/A')}]: ").strip()

        if new_name:
            match['Name'] = new_name
        if new_program:
            meta['program'] = new_program
        if new_contact:
            meta['contact'] = new_contact
        if new_address:
            meta['address'] = new_address

        save_csv_records(csv_records)
        json_data[actual_reg_no] = meta
        save_json_records(json_data)

        print("Success: Student record updated successfully.")
        logging.info(f"Updated record details for Reg No: {actual_reg_no}")

    except StudentNotFoundError as snfe:
        print(f"Update Failed: {snfe.message}")
        logging.warning(f"Update attempt failed: {snfe.message}")
    except Exception as e:
        logging.error(f"Error during update operations: {e}")
        print("Could not update information data.")

def delete_student():
    print("\n--- Delete Student Record ---")
    try:
        reg_no = input("Enter Registration Number to delete: ").strip()
        csv_records = load_csv_records()
        
        match = next((row for row in csv_records if row['Registration Number'].lower() == reg_no.lower()), None)
        if not match:
            raise StudentNotFoundError(reg_no)

        actual_reg_no = match['Registration Number']
        
        confirm = input(f"Are you sure you want to permanently delete {match['Name']}? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion canceled.")
            return

        new_csv_records = [row for row in csv_records if row['Registration Number'].lower() != reg_no.lower()]
        save_csv_records(new_csv_records)

        json_data = load_json_records()
        if actual_reg_no in json_data:
            del json_data[actual_reg_no]
        save_json_records(json_data)

        print(f"Success: Record associated with {actual_reg_no} has been deleted.")
        logging.info(f"Deleted student record: {actual_reg_no}")

    except StudentNotFoundError as snfe:
        print(f"Delete Failed: {snfe.message}")
        logging.warning(f"Delete attempt failed: {snfe.message}")
    except Exception as e:
        logging.error(f"Error during delete operations: {e}")
        print("Could not process record destruction sequence.")

def main():
    initialize_files()
    logging.info("System instance session active.")
    
    while True:
        print("\n========================================")
        print("    STUDENT RECORD MANAGEMENT SYSTEM    ")
        print("========================================")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student by Reg Number")
        print("4. Update Student Details")
        print("5. Delete Student Record")
        print("6. Exit System Application")
        print("========================================")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("\nShutting down system modules. Goodbye!")
            logging.info("System application terminated normally by user.")
            break
        else:
            print("Invalid selection! Please enter a value between 1 and 6.")
            logging.warning(f"User entered invalid navigation choice context: '{choice}'")

if __name__ == '__main__':
    main()