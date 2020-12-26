import sqlite3
from pathlib import Path
from tabulate import tabulate

conn = sqlite3.connect('accounts.db')

c = conn.cursor()

def create_table():
    '''(None)->None
    Creates database in current directory'''
    c.execute("""CREATE TABLE accounts (
                website text,
                username text,
                password text)""")


def insert_account(website, username, password):
    '''(String, String, String)->None
    Inserts website, username, and password into database'''
    data = (website, username, password)
    with conn:
        c.execute("INSERT INTO accounts VALUES (?, ?, ?)", data)
    print("Account added successfully!")


def display_accounts():
    '''(None)->None
    Returns all data from database'''
    c.execute("SELECT * FROM accounts")
    print(tabulate([list(i) for i in c.fetchall()], headers=["Website", "Username", "Password"], tablefmt='orgtbl'))


def update_password(website, username, new_password):
    '''(String, String, String)->None
    Updates password corresponding to given website and username. If given password
    matches the password in the database, the password can be updated '''
    data = (new_password, username, website)
    with conn:
        c.execute("""UPDATE accounts SET password=? WHERE username=? AND website=?""", data)
    print("Password updated successfully!")



def remove_account(website, username, password):
    '''(String, String, String)->None
    Removes an account from the database corresponding to given website, username, and password'''
    data = (website, password, username)
    with conn:
        c.execute("DELETE from accounts WHERE website=? AND password=? AND username=?", data)
    print("Account removed successfully")


def get_from_site(website):
    with conn:
        c.execute("SELECT * FROM accounts WHERE website=?", (website,))
    r = c.fetchone()
    return f"Username: {r[1]}\nPassword: {r[2]}"


def change_system_pass():
    '''(String)->None
    Updates the password associated with accessing the accounts database'''
    password_file = open("pw.txt", "w")
    password_file.write(input("Please input your new password: "))
    password_file.close()
    password_file = open("pw.txt", "r")
    password = password_file.read()
    password_file.close()
    print(f"Password changed successfully.\nYour new password is: {password}")

########
# main #
########

if __name__=="__main__":
    # check if database exists in dir

    try:
        create_table()
    except:
        pass

    # create new password file if it does not already exist

    if not Path("pw.txt").is_file():
        f = open("pw.txt", "w")
        f.write(input("Please input a new password: "))
        f.close()

    # input system password

    password_file = open('pw.txt', 'r')
    password = password_file.read()
    password_file.close()
    password_input = input("Please input your password: ")

    while password != password_input:
        print("Incorrect password.")
        password_input = input("Please input your password: ")

    print("\nLogin successful!")

    running = True

    while running:

        inp = str(input("\nWhat would you like to do?\n[1] Look at all accounts\n[2] Add an account\n[3] Update a password\n[4] Remove an account\n[5] Change login password\n[6] Get account from website\n[7] Exit\n")).strip()

        if inp == '1':
            print("Here are all your accounts:\n")
            display_accounts()

        elif inp == '2': # Adding a new account to the database

            print("\nAdding a new account.\n")
            data = input("Please input the website, username, and password separated by spaces: ").split(' ')
            try:
                insert_account(data[0], data[1], data[2])
            except:
                print("Could not add account to database.")

        elif inp == '3': # Updating a password in the database

            print("\nUpdating account password.\n")
            data = input("Please input the website, username, and new password separated by spaces: ").split(' ')
            try:
                update_password(data[0], data[1], data[2])
            except:
                print("Could not update account password.")

        elif inp == '4': # Remove an account from the database

            print("\nRemoving an account.\n")
            data = input("Please input the website, username, and password separated by spaces: ").split(' ')
            try:
                remove_account(data[0], data[1], data[2])
            except:
                print("Could not remove account from database.")

        elif inp == '5': # Change the password required to access the database

            print("\nChanging system password.\n")
            try:
                change_system_pass()
            except:
                print("Could not change system password.")
        
        elif inp == '6':

            print("\nRetrieving account from website.")
            website = input("Please input website name: ")
            try:
                print(get_from_site(website))
            except:
                print("Could not retrieve account.")

        elif inp == '7': # Exit the program

            print("\nGoodbye.")
            running = False
            conn.close()
        
        else:
            print("\nNot a valid input.\n")
