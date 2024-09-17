from colorama import Fore, Style
from db_functions import (
    display_passwords,
    store_password,
    delete_password,
    update_entry,
)


def main():
    start_menu()


def start_menu():
    print("\n" + "PASSWORD MANAGER".center(30, "="))
    print(
        f"{Fore.YELLOW}1: Display Passwords{Style.RESET_ALL}\n{Fore.GREEN}2: Store Password{Style.RESET_ALL}\n{Fore.RED}3: Delete Password{Style.RESET_ALL}\n{Fore.CYAN}4: Update Entry{Style.RESET_ALL}"
    )
    print("".center(30, "="))

    while True:
        try:
            user_choice = int(input("Enter choice: "))
            if user_choice not in {1, 2, 3, 4}:
                print(f"{Fore.RED}ERROR: Please enter a valid choice{Style.RESET_ALL}")
            else:
                break

        except ValueError:
            print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

    if user_choice == 1:
        display_passwords()
    elif user_choice == 2:
        store_password()
    elif user_choice == 3:
        delete_password()
    else:
        update_entry()


if __name__ == "__main__":
    main()
