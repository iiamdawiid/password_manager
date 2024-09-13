import os
import pymongo
from dotenv import load_dotenv
from colorama import Fore, Style
from password_generator import generate_password
from password_encryption import encrypt_password, decrypt_password

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
password_collection = db[collection_name]


def main():
    start_menu()


def start_menu():
    print("\n" + "PASSWORD MANAGER".center(30, "="))
    print(
        f"{Fore.YELLOW}1: Display Passwords{Style.RESET_ALL}\n{Fore.GREEN}2: Store Password{Style.RESET_ALL}\n{Fore.RED}3: Delete Password{Style.RESET_ALL}"
    )
    print("".center(30, "="))
    while True:
        try:
            user_choice = int(input("Enter choice: "))
            if user_choice not in {1, 2, 3}:
                print("ERROR: Please enter a valid choice")
            else:
                break

        except ValueError:
            print("ERROR: Please enter a number")

    if user_choice == 1:
        display_passwords()

    elif user_choice == 2:
        # complete first
        store_password()

    else:
        delete_password()


def display_passwords():
    # require MASTER PASSWORD for login to ensure security
    print("\n" + "DISPLAY PASSWORDS".center(30, "="))
    master_password = input("Enter master password: ")
    encrypted_maspas = encrypt_password(master_password)
    user = password_collection.find({"master_password": encrypted_maspas})

    user_records = list(user)

    if user:
        for record in user_records:
            # IMPLEMENT TABULATE LIBRARY TO IMPROVE OUTPUT
            master_password = record["master_password"]
            website = record["website_name"]
            password = decrypt_password(record["password"])
            print(
                f"\nMaster password: {master_password}\nWebsite: {website}\nPassword: {password}"
            )
    else:
        print(f"No passwords stored for user")


def store_password():
    # finish first
    print("\n" + "STORE PASSWORD".center(30, "="))
    master_password = input("Enter master password (REMEMBER IT): ")
    encrypted_master_password = encrypt_password(master_password)
    website_name = input("Enter website name (Ex. facebook): ")
    print("".center(30, "="))
    print("1: Enter Personal Password\n2: Generate Secure Password")
    print("".center(30, "="))

    while True:
        try:
            password_choice = int(input("Enter choice:  "))
            if password_choice not in {1, 2}:
                print("ERROR: Valid choices are 1 or 2")
            else:
                break

        except ValueError:
            print("ERROR: Please enter a number")

    if password_choice == 1:
        password = input("Enter password: ")
        print(f"Personal Password: {password}")

    else:
        password = generate_password()
        print(f"Generated Password: {password}")

    # after getting password encrypt it
    encrypted_password = encrypt_password(password)

    # store in db
    website_data = {
        # instead of user, replace with master_password
        "master_password": encrypted_master_password,
        "website_name": website_name,
        "password": encrypted_password,
    }
    password_collection.insert_one(website_data)
    print("Password stored successfully")


def delete_password(): ...


if __name__ == "__main__":
    main()
