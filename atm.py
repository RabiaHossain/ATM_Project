import atm_functions
def main_menu():
 while True:
    
    print("\n\t\t\t\t\t\t\tATM")
    print("Main Menu")
    print("\t1. Create Account")
    print("\t2. Check In")
    print("\t3. Exit")
    
    
    user_choice = int(input("Enter 1 for Cr2eate Account\nEnter 2 for CheckIn\nEnter 3 for Exit"))
    if user_choice == 1:
        atm_functions.create_account()
    elif user_choice == 2:
        atm_functions.input_validation()
    elif user_choice == 3:
        print("Exiting ATM. Thank you!")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")

main_menu()