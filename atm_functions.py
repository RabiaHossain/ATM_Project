import random
import json

def validate_name(name):
    while True:
        if not name.isalpha():
            print("Invalid name. Please enter letters only.")
            name = input("Enter your name: ")
        else:
            return name

def validate_amount(amount):
    while True:
     if amount <=50:
       print("Invalid amount. Please enter amount more than 50")
       amount = int(input("Enter amount you want to deposit: "))
     else:
       return amount

def validate_code(code):
   while True:
    if len(code)> 4 or len(code)<4:
      print("Invalid Code. Please enter 4-digit code")
      code = input("Enter 4 digit pin code: ")
    else:
      return code
    

def generate_unique_username(name):

    cleaned_name = name.lower().replace(" ", "")
    random_number = random.randint(1000, 9999)
    unique_username = cleaned_name + str(random_number)
    return unique_username


def generate_unique_id():
    
    random_number = random.randint(1000000000, 9999999999)
    unique_id = str(random_number)
    return unique_id
    
def account_details():
    user_identifier = input("Enter your unique ID or username: ")
    file = open("users.txt", "r")
    user_info = (file.read())  
    file.close()  

    if user_identifier in user_info:
        user_data = user_info[user_identifier]
        print("User ID:", user_data["id"])
        print("User Name:", user_data["name"])
        print("Username:", user_data["username"])
    else:
        print("User not found. Please enter a valid unique ID or username.")

def check_in(user_id): 
 while True:
    print("\t\t1. Account Details")
    print("\t\t2. Deposit")
    print("\t\t3. Withdraw")
    print("\t\t4. Update Pin")
    print("\t\t5. Check Statement")
    print("\t\t6. Checkout")
    
    submenu_userchoice = int(input("Select Option from 1 to 6: ")) 
    
    if submenu_userchoice == 1:
        account_details(user_id)
    elif submenu_userchoice == 2:
        deposit(user_id)
        
    elif submenu_userchoice == 3:
        withdraw(user_id)
       
    elif submenu_userchoice == 4:
        update_pin(user_id)  
       
    elif submenu_userchoice == 5:
        check_statement(user_id)
        
    elif submenu_userchoice == 6:
        checkout(user_id) 
       
    else:
        print("Invalid choice. Please select a valid option.")


def withdraw(user_id):
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)
    user_data = None
    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break
    if user_data:
        if user_data["status"] == "BLOCKED":
            print("Blocked users cannot withdraw. Please contact customer support to reactivate your account.")
            return
        available_balance = user_data["acc_details"].get("balance", 0)
        for entry in user_data["acc_details"].get("statement", []):
            if entry["type"] == "Deposit":
                available_balance += entry["amount"]
            elif entry["type"] == "Withdrawal":
                available_balance -= entry["amount"] + entry["tax"]
        while True:
            try:
                withdrawal_amount = float(input("Enter the amount you want to withdraw: "))
                tax = withdrawal_amount * 0.01 

                if withdrawal_amount + tax <= available_balance:
                    user_data["acc_details"]["balance"] -= (withdrawal_amount + tax)
                    if "acc_details" in user_data and "statement" in user_data["acc_details"]:
                        user_data["acc_details"]["statement"].append({"type": "Withdrawal", "amount": withdrawal_amount, "tax": tax})
                    else:
                        user_data["acc_details"]["statement"] = [{"type": "Withdrawal", "amount": withdrawal_amount, "tax": tax}]

                    with open("users.txt", "w") as file:
                        json.dump(user_info_list, file)

                    print(f"Withdrawal of {withdrawal_amount} (including 1% tax) successful.")
                    print("Updated balance:", user_data["acc_details"]["balance"])
                    break
                else:
                    print("Insufficient balance. Please enter a lower withdrawal amount.")
            except ValueError:
                print("Invalid input. Please enter a valid amount.")
    else:
        print("User not found. Please enter a valid user ID.")

def main_menu():
 while True:
    
    print("\n\t\t\t\t\t\t\tATM")
    print("Main Menu")
    print("\t1. Create Account")
    print("\t2. Check In")
    print("\t3. Exit")
    
    user_choice = int(input("Enter 1 for Create Account\nEnter 2 for CheckIn\nEnter 3 for Exit"))
    if user_choice == 1:
        create_account()
    elif user_choice == 2:
        input_validation()
    elif user_choice == 3:
        print("Exiting ATM. Thank you!")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")

def save_user_info_to_file(user_info):
    with open('users.txt', 'a') as file:
        json.dump(user_info, file)
        file.write('\n')

def input_validation():
    global user_id
    user_id = input("Enter your user ID: ")
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)
    user_data = None
    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break

    if user_data:
        print("Congratulations, your ID exists!")
        attempt = 0
        while attempt < 3:  
            login_code = input("Enter 4-digit pin code: ")

            if login_code == user_data["pin_code"]:
                print("Login successful!")
                print(check_in(user_id))
                break  
            else:
                attempt += 1
                remaining_attempts = 3 - attempt
                if remaining_attempts > 0:
                    print(f"Pin code does not match! You have {remaining_attempts} more attempts.")
                else:
                    print("You have used all three attempts. Your account is now blocked.")
                    if user_data:
                        user_data["status"] = "BLOCKED"
                        user_info_list[user_info_list.index(user_data)] = user_data
                        with open("users.txt", "w") as file:
                            json.dump(user_info_list, file)
                    break  

        if attempt < 3 and user_data["status"] != "BLOCKED":
            check_in(user_id)
    else:
        print("Your ID does not exist. Please create your account.")

def create_account():
    global user_id
    global username
    global user_info
    user_name = input("Enter your name: ")
    validated_name = validate_name(user_name)
    print(validated_name)
    username = generate_unique_username(validated_name)
    validated_entered = int(input("Enter amount you want to deposit: "))
    deposit_amount = validate_amount(validated_entered)
    print(deposit_amount)
    user_code = input("Enter 4-digit pin code: ")
    global pin_code
    pin_code = validate_code(user_code)
    print(pin_code)

    status = "ACTIVE"
    currency = "PKR"
    statement = [{"type": "Deposit", "amount": deposit_amount}]
    user_id = generate_unique_id()

    user_info = {
        'id': user_id,
        'name': validated_name,
        'username': username,
        'pin_code': pin_code,
        'status': status,
        'acc_details': {
            'currency': currency,
            'statement': statement,
        }
    }
    try:
        with open('users.txt', 'r') as file:
            file_contents = file.read()
            if file_contents.strip(): 
                user_info_list = json.loads(file_contents)
            else:
                user_info_list = []  
    except FileNotFoundError:
        user_info_list = []

    user_info_list.append(user_info)
    with open('users.txt', 'w') as file:
        json.dump(user_info_list, file)

    print("Account created successfully!")
    print(f"Your User name is : {username}")
    print(f"Your User id is : {user_id}")

def account_details(user_id):
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)
    user_data = None

    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break

    if user_data:
        print("\nAccount Details:")
        print("Name:", user_data["name"])
        print("Username:", user_data["username"])
        print("Status:", user_data["status"])
        print("Account Details:", user_data["acc_details"])
        
    else:
        print("User not found. Please enter a valid user ID.")
def deposit(user_id):
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)

    user_data = None

    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break

    if user_data:
     while True:
        try:
            deposit_amount = float(input("Enter the amount you want to deposit (must be at least 50): "))

            if deposit_amount < 50:
                print("Invalid amount. Please enter an amount of 50 or more.")
            else:
                if "acc_details" not in user_data:
                    user_data["acc_details"] = {}
                
                if "balance" not in user_data["acc_details"]:
                    user_data["acc_details"]["balance"] = deposit_amount 

                user_data["acc_details"]["balance"] += deposit_amount

                if "statement" not in user_data["acc_details"]:
                    user_data["acc_details"]["statement"] = []

                user_data["acc_details"]["statement"].append({"type": "Deposit", "amount": deposit_amount})

                with open("users.txt", "w") as file:
                    json.dump(user_info_list, file)

                print(f"Deposit of {deposit_amount} successful.")
                print("Updated balance:", user_data["acc_details"]["balance"])
                break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    else:
        print("User not found. Please enter a valid user ID.")


def update_pin(user_id):
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)
    user_data = None

    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break

    if user_data:
        previous_pin = input("Enter your previous 4-digit PIN: ")
        if previous_pin == user_data["pin_code"]:
            new_pin = input("Enter your new 4-digit PIN: ")
            user_data["pin_code"] = new_pin
            with open("users.txt", "w") as file:
                json.dump(user_info_list, file)

            print("PIN update successful!")
        else:
            print("Incorrect previous PIN. PIN update failed.")
    else:
        print("User not found. Please enter a valid user ID.")


def check_statement(user_id):
    with open("users.txt", "r") as file:
        user_info_list = json.load(file)
    user_data = None
    for user_data_obj in user_info_list:
        if user_data_obj["id"] == user_id:
            user_data = user_data_obj
            break

    if user_data:
        if "acc_details" in user_data and "statement" in user_data["acc_details"]:
            statement = user_data["acc_details"]["statement"]
            formatted_entries = [f"You {entry['type']} Rs {entry['amount']}" for entry in statement]
            print("Account Statement:", formatted_entries)
        else:
            print("No statement available for this user.")
    else:
        print("User not found. Please enter a valid user ID.")

def checkout(user_id):
    print("Logged out successfully!")
    main_menu()
    