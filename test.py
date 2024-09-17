def display_passwords(display_header=True):
    if display_header:
        print(
            f"\n{Fore.YELLOW}{'DISPLAY PASSWORDS'.center(30, '=')}{Style.RESET_ALL}"
        )

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
                password = decrypt_password(record["password"])
                table.append([website, password])
            break

        else:
            print(f"LOGIN: {Fore.RED}FAILED{Style.RESET_ALL}")
            print(f"{Fore.RED}No passwords stored for user{Style.RESET_ALL}")

    print(tabulate(table, headers=["website", "password"]))