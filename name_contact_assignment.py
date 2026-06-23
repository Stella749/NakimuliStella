import re

class ContactManager:
    def __init__(self):

        self.contacts = {}
        self.current_id = 1

    def _is_valid_phone(self, phone):
        """Validates that phone contains only digits, hyphens, and optional leading plus."""

        cleaned = phone.replace("+", "").replace("-", "")
        return cleaned.isdigit() and len(cleaned) > 0

    def _is_valid_email(self, email):
        """Validates basic email structure containing '@' and '.'."""
        if not email:
            return True  
        return "@" in email and "." in email

    def add_contact(self, name, phone, email=""):
        
        if not self._is_valid_phone(phone):
            print("\n Error: Invalid phone number. Only digits and hyphens are allowed.")
            return False
        if not self._is_valid_email(email):
            print("\n Error: Invalid email address. Must contain '@' and '.'.")
            return False

        
        self.contacts[self.current_id] = {
            "name": name,
            "phone": phone,
            "email": email
        }
        print(f"\n Contact added successfully! (ID: {self.current_id})")
        self.current_id += 1
        return True

    def view_contact(self, contact_id):
        if contact_id in self.contacts:
            c = self.contacts[contact_id]
            print(f"\n--- Contact Details (ID: {contact_id}) ---")
            print(f"Name:  {c['name']}")
            print(f"Phone: {c['phone']}")
            print(f"Email: {c['email'] if c['email'] else 'N/A'}")
        else:
            print("\n Error: Contact ID not found.")

    def update_contact(self, contact_id, name=None, phone=None, email=None):
        if contact_id not in self.contacts:
            print("\n Error: Contact ID not found.")
            return False

        # Pre-validate if new data is provided
        if phone and not self._is_valid_phone(phone):
            print("\n Error: Invalid phone number. Operation cancelled.")
            return False
        if email and not self._is_valid_email(email):
            print("\n Error: Invalid email address. Operation cancelled.")
            return False

        
        if name:
            self.contacts[contact_id]['name'] = name
        if phone:
            self.contacts[contact_id]['phone'] = phone
        if email is not None:  # Allows clearing email if passed as empty string
            self.contacts[contact_id]['email'] = email

        print(f"\n Contact ID {contact_id} updated successfully!")
        return True

    def delete_contact(self, contact_id):
        if contact_id in self.contacts:
            deleted_name = self.contacts[contact_id]['name']
            del self.contacts[contact_id]
            print(f"\n Contact '{deleted_name}' deleted successfully.")
            return True
        print("\n Error: Contact ID not found.")
        return False

    def list_all_contacts(self):
        if not self.contacts:
            print("\n Your contact book is currently empty.")
            return

        results = [(cid, info['name'], info['phone'], info['email']) for cid, info in self.contacts.items()]
        self._print_formatted_results(results, "All Contacts")

    def search_contacts(self, query):
        """Searches by name, phone, or email (case-insensitive)."""
        query = query.lower()
        results = []

        for cid, info in self.contacts.items():
            if (query in info['name'].lower() or 
                query in info['phone'] or 
                query in info['email'].lower()):
                results.append((cid, info['name'], info['phone'], info['email']))
        
        self._print_formatted_results(results, f"Search Results for '{query}'")
        return results

    def _print_formatted_results(self, raw_results, title):
        """Helper method to format search results and list views cleanly."""
        print(f"\n=== {title} ===")
        if not raw_results:
            print("No matching contacts found.")
            print("=" * (len(title) + 8))
            return

        print(f"{'ID':<5} | {'Name':<20} | {'Phone':<15} | {'Email':<25}")
        print("-" * 75)
        for cid, name, phone, email in raw_results:
            email_display = email if email else "N/A"
            print(f"{cid:<5} | {name:<20} | {phone:<15} | {email_display:<25}")
        print("=" * 75)

def main():
    manager = ContactManager()

    while True:
        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")
        
        choice = input("Choose an option (1-7): ").strip()

        if choice == '1':
            name = input("Enter Name: ").strip()
            phone = input("Enter Phone (e.g., +256-701): ").strip()
            email = input("Enter Email (Optional): ").strip()
            if name and phone:
                manager.add_contact(name, phone, email)
            else:
                print("\n Error: Name and Phone are required fields.")

        elif choice == '2':
            try:
                cid = int(input("Enter Contact ID to view: "))
                manager.view_contact(cid)
            except ValueError:
                print("\n Error: Please enter a valid numerical ID.")

        elif choice == '3':
            try:
                cid = int(input("Enter Contact ID to update: "))
                if cid not in manager.contacts:
                    print("\n Error: Contact ID not found.")
                    continue
                
                print("(Leave blank and press Enter to keep current value)")
                name = input("Enter New Name: ").strip()
                phone = input("Enter New Phone: ").strip()
                email = input("Enter New Email: ").strip()
                
                # Only pass parameters that the user actually wanted to change
                manager.update_contact(
                    contact_id=cid,
                    name=name if name else None,
                    phone=phone if phone else None,
                    email=email if email else None
                )
            except ValueError:
                print("\n Error: Please enter a valid numerical ID.")

        elif choice == '4':
            try:
                cid = int(input("Enter Contact ID to delete: "))
                manager.delete_contact(cid)
            except ValueError:
                print("\n Error: Please enter a valid numerical ID.")

        elif choice == '5':
            query = input("Enter name, phone, or email to search: ").strip()
            if query:
                manager.search_contacts(query)
            else:
                print("\n Error: Search query cannot be empty.")

        elif choice == '6':
            manager.list_all_contacts()

        elif choice == '7':
            print("\nThank you for using Contact Manager. Goodbye!")
            break
            
        else:
            print("\n Error: Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()