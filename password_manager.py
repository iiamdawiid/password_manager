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
                print(f"{Fore.RED}ERROR: Please enter a valid choice{Style.RESET_ALL}")
            else:
                break

        except ValueError:
            print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

    if user_choice == 1:
        display_passwords()

    elif user_choice == 2:
        # complete first
        store_password()

    else:
        delete_password()


def display_passwords(delete_password=False):
    # print only if this function is not called from delete_password
    if not delete_password:
        print(
            "\n"
            + f"{Fore.YELLOW}{'DISPLAY PASSWORDS'.center(30, '=')}{Style.RESET_ALL}"
        )

    # require MASTER PASSWORD for login to ensure security
    while True:
        master_password = input("Enter master password: ")
        encrypted_maspas = encrypt_password(master_password)
        user = password_collection.find({"master_password": encrypted_maspas})

        user_records = list(user)

        if user_records:
            print(f"LOGIN: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
            print(
                "\n"
                + f'{Fore.GREEN}{"SAVED PASSWORDS".center(30, "=")}{Style.RESET_ALL}'
            )
            for record in user_records:
                # IMPLEMENT TABULATE LIBRARY TO IMPROVE OUTPUT
                master_password = record["master_password"]
                website = record["website_name"]
                password = decrypt_password(record["password"])
                print(f"{website}: {Fore.YELLOW}{password}{Style.RESET_ALL}\n")
            break

        else:
            print(f"LOGIN: {Fore.RED}FAILED{Style.RESET_ALL}")
            print(f"{Fore.RED}No passwords stored for user{Style.RESET_ALL}")


def store_password():
    # finish first
    print("\n" + "STORE PASSWORD".center(30, "="))
    master_password = input("Enter master password (REMEMBER IT): ")
    encrypted_master_password = encrypt_password(master_password)
    website_name = input("Enter website name (Ex. facebook): ")
    print("".center(30, "="))
    print(
        f"{Fore.YELLOW}1: Enter Personal Password{Style.RESET_ALL}\n{Fore.GREEN}2: Generate Secure Password{Style.RESET_ALL}"
    )
    print("".center(30, "="))

    while True:
        try:
            password_choice = int(input("Enter choice:  "))
            if password_choice not in {1, 2}:
                print(f"{Fore.RED}ERROR: Valid choices are 1 or 2{Style.RESET_ALL}")
            else:
                break

        except ValueError:
            print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

    if password_choice == 1:
        password = input("Enter password: ")
        print(f"Personal Password: {password}")

    else:
        password = generate_password()
        print(f"Generated Password: {Fore.GREEN}{password}{Style.RESET_ALL}")

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
    print(f"PASSWORD STORED: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")


def delete_password():
    print("\n" + f"{Fore.RED}{'DELETE PASSWORD'.center(30, '=')}{Style.RESET_ALL}")
    display_passwords(True)
    # display selected entry user desires to delete
    while True:
        try:
            website_name = input("Site associated with password: ")
            display_choice = password_collection.find_one(
                {"website_name": website_name}
            )
            if display_choice:
                password_collection.delete_one({"website_name": website_name})
                print(f"DELETE: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
                break
            else:
                print(f"DELETE: {Fore.RED}FAILED{Style.RESET_ALL}")
                print(
                    f"Website '{website_name}' not found: Please double-check and try again."
                )

        except Exception as e:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {e}")


if __name__ == "__main__":
    main()
