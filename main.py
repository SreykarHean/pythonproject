# main.py
import auth
import console_mode

username = input("Username: ")
password = input("Password: ")

role = auth.login(username, password)   # returns "admin" or "user"

if role:
    print(f"Welcome {username}! You are logged in as {role}.")
    console_mode.console_menu(role)     # pass role into menu
else:
    print("Invalid credentials.")
