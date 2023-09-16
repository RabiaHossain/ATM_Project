ATM- Project

Two python files are attached in folder, atm.py contain the main menu and import atm_functions, in atm_functions.py all functions for main menu and 
sub menu are declared. 

Functions:

main_menu(): Displays the main menu for the ATM system.

validate_name(name): Validates the user's name, ensuring it contains only letters.

validate_amount(amount): Validates the amount entered for deposit or withdrawal, ensuring it's more than 50.

validate_code(code): Validates the 4-digit PIN code.

generate_unique_username(name): Generates a unique username based on the user's name.

generate_unique_id(): Generates a unique user ID.

account_details(user_id): Displays user account details.

check_in(user_id): Provides a submenu for banking operations.

withdraw(user_id): Allows the user to withdraw money from their account.

save_user_info_to_file(user_info): Saves user information to a file(users.txt).

input_validation(): Handles user input and authentication.

create_account(): Creates a new user account.

update_pin(user_id): Allows the user to update their PIN code.

check_statement(user_id): Displays the user's account statement.

checkout(user_id): Logout the user from submenu.

deposit(user_id): Allows the user to deposit money into their account.