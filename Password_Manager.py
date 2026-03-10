import os 
import hashlib
import getpass
import json
import string

#Create a file path in the user's home directory to store account data
#This ensuresthe JSON file persists even after the program closes
file_path = os.path.join(os.path.expanduser("~"), "users.json")
weak_file = os.path.join(os.path.dirname(__file__), "common_passwords.json")
# Dictionary to temporarily store usernames and hashed passwords in memory
password_list = {}


def password_validation(userpassword):
    '''
    Validates the strength of a user password.
    Criteria:
    - Minimum 8 characters 
    - Conntains at least one number
    - Contains at least one symbol
    Returns True if valid and False otherwise.
    '''
    #Checks against a list of common/weak passwords
    if len(userpassword) < 8:
        print("Password must be higher than eight characters. Please try again.")
        return False

    with open(weak_file, "r") as weak_passwords:
        data = json.load(weak_passwords)
    
    if userpassword in data:
        print("Password is too simple. Please Try again.")
        return False
    
    #Ensure password contains at least one digit
    if not any(char.isdigit() for char in userpassword):
        print("Password must include at least one number.")
        return False
    
    #Ensure password contains at least one symbol.
    if not any(char in string.punctuation for char in userpassword):
        print("Password must include at least one symbol.")
        return False
    

    print('=== Account successfully created. Thank you ===')
    return True

def creating_account():
    '''
    Handles new account creation
    - Checks if username already exists 
    - Validates password strength
    - Hashes password using SHA-256
    - Stores Credentials in JSON file
    ''' 
    print("==== PLEASE WAIT ====")
    usernameInput = input("Please enter a username: ")

    # Prevents duplicate account creation for securtity reasons.
    if usernameInput in password_list:
        print("Invalid. Account already exists.")
        return
    print(f' \n WELCOME {(usernameInput)}. \n === CREATE AN ACCOUNT === \nCriteria for password : \n Must be moderate. \n Higher than 8 characters \n Must include numbers and symbols. ')
    
    # getpass hides password input from the screen for security
    userpassword = getpass.getpass("Enter new Password:")
    userpasswordconfirmation = getpass.getpass("Confirm password:") 
    
    # Confirm both passwords match
    if userpasswordconfirmation == userpassword:
        # Validates password strength
        if not password_validation(userpassword):
            return
        
        # Hash the password before storing it 
        # This prevents storing plain text passwords for enhanced security
        password_hider =  hashlib.sha256(userpassword.encode()).hexdigest()
        # Store username and hashed password in dictiionary
        password_list[usernameInput] = password_hider

        # save updated dictionary to JSON file
        with open(file_path, 'w') as file:
            json.dump(password_list, file)
         
    else:
        print("Passwords do not match. Please Try again.")

def deleting_account():
    '''
    Deletes an exisitng accounts.
    - Verifies username exists
    - Confirms password before deletion
    - Updates JSON file after removal
    '''
    usernameInput = input("Please enter a username: ")
    if usernameInput in password_list:
        userpassword = getpass.getpass("Enter The Password: ")

        # Hash entered password to compare with stored hash
        password_hider =  hashlib.sha256(userpassword.encode()).hexdigest()

        #Verfify password before deleting account
        if password_list[usernameInput] == password_hider:
            del password_list[usernameInput]
            
            #Save updated dictionary to file
            with open(file_path, 'w') as file:
                json.dump(password_list, file)
            print('Account succesfully deleted.')
    else:
        print("Account does not exists. Operation cancelled.")
   

def login():
    '''
    Handles user login.
    - Prompts for username and password
    - Hashes entered password 
    - Comparers hash to stored value
    '''
    print("==== PLEASE WAIT ====")
    usernameInput = input("Please enter a username: ")
    userpassword = getpass.getpass("Enter Password:")

    # Hash entered password for secure comparision
    password_hider =  hashlib.sha256(userpassword.encode()).hexdigest()

    # Check both username existence and password match
    if usernameInput in password_list and password_list[usernameInput] == password_hider:
        print('Login successful! ')
    else: 
        print("Account does not exist. Please Create account to proceed .")
    
def main():
    '''
    Main program loop.
    Displays menu options and routes user to selected functionality.
    Runs continuously until user selects Exits.
    '''
    while True:
        print(f"==== WELCOME  ====")
        print(f'What would you like to do today?')
        userInput = input("1. Create an account \n2. Login in to an existing account \n3. Delete an existing account \n4. Exit \n")
        if userInput == "1":
            creating_account()
        elif userInput == '2':
            login()
        elif userInput == '3':
            deleting_account()
        elif userInput == '4':
            break
        else:
            print("Invalid response")
        

# Load existing user data from JSON file when program starts 
# This ensures previously created accounts are not lost.
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        password_list = json.load(file)
else:
    password_list = {}


if __name__ == "__main__":
    main()
