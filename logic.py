from pymongo import MongoClient
from InquirerPy  import inquirer
import bcrypt
import jwt
from datetime import datetime, timedelta
from colorama import Fore, Style
from tabulate import tabulate
from mongo_starter import start_mongodb, stop_mongodb_server
try:
    start_mongodb()
except:
    print("MongoDB need to start")
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("contact_management")

users_collection = db.get_collection("users")
contacts_collection = db.get_collection("contacts")

SECRET_KEY = "your_secret_key"

def generate_token(username):
    return jwt.encode(
        {"username": username, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if users_collection.find_one({"username": username}):
        print("User already exists!")
        return None

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_password})
    print("User registered successfully!")

def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = users_collection.find_one({"username": username})
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        print(Fore.RED + "Invalid Username or Password." + Style.RESET_ALL)
        return None

    print(Fore.GREEN+"Login successful!" + Style.RESET_ALL)
    return generate_token(username)

def add_contact(token):
    username = verify_token(token)["username"]
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    contacts_collection.insert_one({"username": username, "name": name, "email": email, "phone": phone})
    print(Fore.GREEN+"Contact successfully added!" + Style.RESET_ALL)

def view_contacts(token):
    username = verify_token(token)["username"]
    contacts = list(contacts_collection.find({"username": username}, {"_id": 0, "username": 0}))
    if contacts:
        headers = [Fore.CYAN + "Name" + Style.RESET_ALL,
                   Fore.CYAN + "Email" + Style.RESET_ALL,
                   Fore.CYAN + "Phone" + Style.RESET_ALL,
        ]
        table_data = [[contact["name"], contact["email"], contact["phone"]] for contact in contacts]
        print(Fore.GREEN + tabulate(table_data, headers, tablefmt="fancy_grid") + Style.RESET_ALL)
    else:
        print(Fore.RED + "No contacts found." + Style.RESET_ALL)
def update_contact(token):
    username = verify_token(token)["username"]
    contacts = list(contacts_collection.find({"username": username}, {"_id": 0, "username": 0}))
    
    if not contacts:
        print(Fore.RED + "No contacts found to update." + Style.RESET_ALL)
        return

    # Display contacts with indexing
    headers = [Fore.CYAN + "Index" + Style.RESET_ALL,
               Fore.CYAN + "Name" + Style.RESET_ALL,
               Fore.CYAN + "Email" + Style.RESET_ALL,
               Fore.CYAN + "Phone" + Style.RESET_ALL]
    table_data = [[i, contact["name"], contact["email"], contact["phone"]] for i, contact in enumerate(contacts)]
    print(Fore.GREEN + tabulate(table_data, headers, tablefmt="fancy_grid") + Style.RESET_ALL)
    
    # Ask for the index of the contact to update
    try:
        index = int(input("Enter the index of the contact to update: "))
        if index < 0 or index >= len(contacts):
            print(Fore.RED + "Invalid index." + Style.RESET_ALL)
            return
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)
        return

    # Get selected contact details
    selected_contact = contacts[index]
    
    print(Fore.YELLOW + "Leave fields blank to keep the current value." + Style.RESET_ALL)
    name = input(f"Name [{selected_contact['name']}]: ") or selected_contact['name']
    phone = input(f"Phone [{selected_contact['phone']}]: ") or selected_contact['phone']

    # Update the contact in the database
    result = contacts_collection.update_one(
        {"username": username, "email": selected_contact["email"]},
        {"$set": {"name": name, "phone": phone}}
    )
    
    if result.matched_count:
        print(Fore.GREEN + "Contact updated successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Failed to update contact." + Style.RESET_ALL)

def search_contact(token):
    username = verify_token(token)["username"]
    query = input("Enter name, email, or phone to search: ")
    contacts = list(contacts_collection.find(
        {"username": username, "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}},
            {"phone": {"$regex": query, "$options": "i"}}
        ]},
        {"_id": 0, "username": 0}
    ))
    if contacts:
        headers = [Fore.CYAN + "Name" + Style.RESET_ALL,
                   Fore.CYAN + "Email" + Style.RESET_ALL,
                   Fore.CYAN + "Phone" + Style.RESET_ALL]
        table_data = [[contact["name"], contact["email"], contact["phone"]] for contact in contacts]
        print(Fore.GREEN + tabulate(table_data, headers, tablefmt="fancy_grid") + Style.RESET_ALL)
    else:
        print(Fore.RED + "No matching contacts found." + Style.RESET_ALL)

def delete_contact(token):
    username = verify_token(token)["username"]
    email = input("Enter the email of the contact to delete: ")
    result = contacts_collection.delete_one({"username": username, "email": email})
    if result.deleted_count:
        print(Fore.GREEN + "Contact deleted successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "No contact found with the given email." + Style.RESET_ALL)


def main():
    token = None
    while True:
        if not token:
            # Menu for unauthenticated users
            choice = inquirer.select(
                message="Choose an option:",
                choices=["Register", "Login", "Exit"],
            ).execute()

            if choice == "Register":
                register_user()
            elif choice == "Login":
                token = login_user()
            elif choice == "Exit":
                print("Goodbye!")
                stop_mongodb_server()
                break
        else:
            # Menu for authenticated users
            choice = inquirer.select(
                message="Choose an option:",
                choices=["Add Contact", "View Contacts", "Update", "Search", "Delete", "Logout"],
            ).execute()

            if choice == "Add Contact":
                add_contact(token)
            elif choice == "View Contacts":
                view_contacts(token)
            elif choice == "Update":
                update_contact(token)
            elif choice == "Search":
                search_contact(token)
            elif choice == "Delete":
                delete_contact(token)
            
            elif choice == "Logout":
                token = None  # Logout
                print("Logged out successfully!")
if __name__ == "__main__":
    main()
