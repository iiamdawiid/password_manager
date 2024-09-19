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
    while True:
        print("\n" + "PASSWORD MANAGER".center(20, "="))
        print(
            f"{Fore.YELLOW}1: Display{Style.RESET_ALL}\n{Fore.GREEN}2: Store{Style.RESET_ALL}\n{Fore.CYAN}3: Update{Style.RESET_ALL}\n{Fore.RED}4: Delete{Style.RESET_ALL}\n{Fore.RED}5: Quit{Style.RESET_ALL}"
        )
        print("".center(20, "="))

        while True:
            try:
                user_choice = int(input("Enter choice: "))
                if user_choice not in {1, 2, 3, 4, 5}:
                    print(
                        f"{Fore.RED}ERROR: Please enter a valid choice{Style.RESET_ALL}"
                    )
                else:
                    break

            except ValueError:
                print(f"{Fore.RED}ERROR: Please enter a number{Style.RESET_ALL}")

        if user_choice == 1:
            display_passwords()
        elif user_choice == 2:
            store_password()
        elif user_choice == 3:
            update_entry()
        elif user_choice == 4:
            delete_password()
        else:
            print(f"{Fore.RED}PROGRAM QUIT{Style.RESET_ALL}")
            break

        while True:
            try:
                go_again = input(
                    f"\nPress {Fore.GREEN}'C'{Style.RESET_ALL} to {Fore.GREEN}continue{Style.RESET_ALL} or {Fore.RED}'Q'{Style.RESET_ALL} to {Fore.RED}quit{Style.RESET_ALL}: "
                )
                go_again = go_again.upper()
                if go_again not in {"C", "Q"}:
                    print(f"{Fore.RED}ERROR: Please enter 'C' or 'Q'{Style.RESET_ALL}")
                else:
                    break

            except Exception as e:
                print(f"ERROR: {e}")

        if go_again == "C":
            continue
        else:
            print(f"{Fore.RED}PROGRAM QUIT{Style.RESET_ALL}")
            break


if __name__ == "__main__":
    main()
