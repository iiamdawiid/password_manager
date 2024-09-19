import os
import pymongo
from tabulate import tabulate
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


def display_passwords(display_header=True):
    if display_header:
        print(f"\n{Fore.YELLOW}{'DISPLAY PASSWORDS'.center(30, '=')}{Style.RESET_ALL}")

    while True:
        master_password = input("Enter master password: ")
        encrypted_maspas = encrypt_password(master_password)
        user = password_collection.find({"master_password": encrypted_maspas})

        user_records = list(user)
        table = []

        if user_records:
            print(f"LOGIN: {Fore.GREEN}SUCCESS{Style.RESET_ALL}\n")
            for record in user_records:
                website = record["website_name"]
                password = f"{Fore.YELLOW}{decrypt_password(record['password'])}{Style.RESET_ALL}"
                table.append([website, password])
            break

        else:
            print(f"LOGIN: {Fore.RED}FAILED{Style.RESET_ALL}")
            print(f"{Fore.RED}No passwords stored for user{Style.RESET_ALL}")

    head1fmt = f"{Fore.GREEN}WEBSITE{Style.RESET_ALL}"
    head2fmt = f"{Fore.GREEN}PASSWORD{Style.RESET_ALL}"

    print(tabulate(table, headers=[head1fmt, head2fmt], tablefmt="github"))


def store_password():
    print(f"\n{Fore.GREEN}{'STORE PASSWORD'.center(40, '=')}{Style.RESET_ALL}")
    master_password = input("Enter master password (REMEMBER IT): ")
    encrypted_master_password = encrypt_password(master_password)
    website_name = input("Enter website name (Ex. facebook): ")
    print("".center(40, "="))
    print(
        f"{Fore.YELLOW}1: Enter Personal Password{Style.RESET_ALL}\n{Fore.GREEN}2: Generate Secure Password{Style.RESET_ALL}"
    )
    print("".center(40, "="))

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

    encrypted_password = encrypt_password(password)

    # info that is stored in db
    website_data = {
        "master_password": encrypted_master_password,
        "website_name": website_name,
        "password": encrypted_password,
    }

    password_collection.insert_one(website_data)
    print(f"PASSWORD STORED: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")


def delete_password():
    print(f"\n{Fore.RED}{'DELETE PASSWORD'.center(30, '=')}{Style.RESET_ALL}")
    display_passwords(False)
    print("".center(40, "="))

    while True:
        try:
            website_name = input("Site associated with password: ")
            delete_choice = password_collection.find_one({"website_name": website_name})

            if delete_choice:
                while True:
                    try:
                        confirm_delete = input(
                            f"Enter {Fore.RED}'DELETE {website_name}'{Style.RESET_ALL} to {Fore.RED}delete{Style.RESET_ALL} or {Fore.GREEN}'Q'{Style.RESET_ALL} to {Fore.GREEN}quit{Style.RESET_ALL}: "
                        )
                        delete_phrase = f"DELETE {website_name}"
                        if confirm_delete == delete_phrase:
                            password_collection.delete_one(
                                {"website_name": website_name}
                            )
                            print(f"DELETE: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
                            break
                        elif confirm_delete == "Q":
                            print(f"{Fore.RED}PROGRAM QUIT{Style.RESET_ALL}")
                            break
                        else:
                            print(
                                f"{Fore.RED}SPELLING ERROR: Please try again{Style.RESET_ALL}"
                            )

                    except Exception as e:
                        print(f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}")
                break
            else:
                print(f"DELETE: {Fore.RED}FAILED{Style.RESET_ALL}")
                print(
                    f"Website '{website_name}' not found: Please double-check and try again."
                )
        except Exception as e:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {e}")


def update_entry():
    print(f"\n{Fore.CYAN}{'UPDATE ENTRY'.center(30, '=')}{Style.RESET_ALL}")
    # call display_passwords() and display stored passwords, if any
    display_passwords(False)
    # ask user to select an entry by website_name
    while True:
        try:
            print("".center(40, "="))
            website_name = input("Choose entry by website name: ")
            user_selection = password_collection.find_one(
                {"website_name": website_name}
            )
            if user_selection:  # website exists in db
                break
            else:
                print(
                    f"{Fore.RED}Website '{website_name}' was not found: Please double-check and try again.{Style.RESET_ALL}"
                )

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    print("".center(40, "="))
    while True:
        try:
            update_choice = int(
                input(
                    f"{Fore.GREEN}1: Update website{Style.RESET_ALL}    {Fore.GREEN}2: Update password{Style.RESET_ALL}\nEnter choice: "
                )
            )
            if update_choice not in {1, 2}:
                print(f"{Fore.RED}ERROR: Please enter 1 or 2 {Style.RESET_ALL}")
            else:
                break

        except ValueError:
            print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

    print("".center(40, "="))
    if update_choice == 1:
        new_website_name = input("Enter new website name: ")
        while True:
            try:
                confirm_website_name = input("Confirm website name: ")
                if new_website_name == confirm_website_name:
                    password_collection.update_one(
                        {"website_name": website_name},
                        {"$set": {"website_name": new_website_name}},
                    )
                    print(f"UPDATE: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
                    break
                else:
                    print(
                        f"{Fore.RED}ERROR: Website name's do not match. Please try again{Style.RESET_ALL}"
                    )

            except Exception as e:
                print(f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}")

    else:
        while True:
            try:
                password_choice = int(
                    input(
                        f"{Fore.YELLOW}1: Enter Personal Password{Style.RESET_ALL}\n{Fore.GREEN}2: Generate Secure Password{Style.RESET_ALL}\nEnter choice: "
                    )
                )
                if password_choice not in {1, 2}:
                    print(f"{Fore.RED}ERROR: Please enter 1 or 2{Style.RESET_ALL}")
                else:
                    break

            except ValueError:
                print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

        print("".center(40, "="))
        if password_choice == 1:
            new_password = input("Enter new password: ")
            while True:
                try:
                    confirm_new_password = input("Confirm new password: ")
                    if new_password == confirm_new_password:
                        password_collection.update_one(
                            {"website_name": website_name},
                            {"$set": {"password": encrypt_password(new_password)}},
                        )
                        print(f"UPDATE: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
                        break
                    else:
                        print(
                            f"{Fore.RED}ERROR: Passwords do not match. Please try again{Style.RESET_ALL}"
                        )

                except Exception as e:
                    print(f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}")

        else:
            new_password = generate_password()
            print(f"Generated Password: {Fore.GREEN}{new_password}{Style.RESET_ALL}")
            password_collection.update_one(
                {"website_name": website_name}, {"$set": {"password": new_password}}
            )
            print(f"UPDATE: {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
