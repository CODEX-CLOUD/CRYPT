import os
import time
import sys
import random
from tkinter import filedialog, messagebox
from tkinter import Tk
from cryptography.fernet import Fernet
import json

# Constants
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "password"
CREDENTIALS_FILE = "credentials.json"
ENCRYPTION_KEY_FILE = "key.key"
CRYPTED_FILES_FOLDER = "crypted_files"


# Function to display ASCII art
def display_ascii_art():
    ascii_art = """
   ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
  ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
  ╚██████╗██║  ██║   ██║   ██║        ██║   
   ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
"""
    print(ascii_art)


# Function to log in
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
        print("\nAccess Granted!")
        make_it_snow("Access Granted!")
        return True
    else:
        print("\nAccess Denied!")
        sys.exit(0)



# Function to generate a snowfall animation with 1s and 0s
def make_it_snow(text):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
    columns = 80
    rows = 20

    for _ in range(30):  # Animation duration
        print("\n" * rows)
        for _ in range(rows):
            line = "".join(str(random.choice([0, 1])) for _ in range(columns))
            print(line)
        print("\n" * 5 + f"{text.center(columns, ' ')}")
        time.sleep(0.05)
        os.system('cls' if os.name == 'nt' else 'clear')


# Generate encryption key if not existing
def generate_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("Encryption key generated successfully.")


# Load encryption key
def load_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        print("Error: Encryption key file not found.")
        sys.exit(1)
    with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
        return key_file.read()


def encrypt_file(filename, username, password):
    key = load_key()
    fernet = Fernet(key)

    # Read file content
    with open(filename, "rb") as file:
        original_content = file.read()

    # Encrypt content
    encrypted_content = fernet.encrypt(original_content)

    # Save encrypted content to file
    os.makedirs(CRYPTED_FILES_FOLDER, exist_ok=True)
    crypted_filepath = os.path.abspath(os.path.join(CRYPTED_FILES_FOLDER, os.path.basename(filename) + ".crypt"))
    with open(crypted_filepath, "wb") as encrypted_file:
        encrypted_file.write(encrypted_content)

    # Save credentials for this file
    credentials = {}
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as credentials_file:
                credentials = json.load(credentials_file)
        except json.JSONDecodeError:
            print("Warning: Credentials file is corrupted. Resetting it.")
            credentials = {}

    # Use normalized file path as the key
    credentials[crypted_filepath] = {"username": username, "password": password}

    with open(CREDENTIALS_FILE, "w") as credentials_file:
        json.dump(credentials, credentials_file, indent=4)

    print(f"File '{filename}' has been encrypted and saved at '{crypted_filepath}'.")

#decrypts files
def decrypt_file(filename, username, password):
    normalized_filename = os.path.abspath(filename)
    print(f"Debug: Normalized filename for decryption: {normalized_filename}")

    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print("Error: Credentials file not found.")
        return

    # Load and validate credentials
    try:
        with open(CREDENTIALS_FILE, "r") as credentials_file:
            credentials = json.load(credentials_file)

        if normalized_filename in credentials:
            stored_username = credentials[normalized_filename]["username"]
            stored_password = credentials[normalized_filename]["password"]

            print(f"Debug: Stored username: {stored_username}, provided username: {username}")
            print(f"Debug: Stored password: {stored_password}, provided password: {password}")

            if username.lower() != stored_username.lower() or password != stored_password:
                print("Error: Invalid username or password!")
                return
        else:
            print(f"Error: File '{normalized_filename}' not found in credentials!")
            return
    except json.JSONDecodeError:
        print("Error: Credentials file is corrupted.")
        return

    print("Credentials validated. Proceeding with decryption...")

    # Load encryption key and decrypt
    key = load_key()
    fernet = Fernet(key)

    # Read encrypted file content
    try:
        with open(filename, "rb") as encrypted_file:
            encrypted_content = encrypted_file.read()

        # Decrypt content
        original_content = fernet.decrypt(encrypted_content)

        decrypted_filepath = filename.replace(".crypt", "_decrypted")
        with open(decrypted_filepath, "wb") as decrypted_file:
            decrypted_file.write(original_content)

        print(f"File '{filename}' has been decrypted and saved as '{decrypted_filepath}'.")
    except Exception as e:
        print(f"Error: Decryption failed. {e}")


# Main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Encrypt a File")
        print("2. Decrypt a File")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            root = Tk()
            root.withdraw()
            file_to_encrypt = filedialog.askopenfilename(title="Select a file to encrypt")
            if file_to_encrypt:
                user = input("Set a username for this encrypted file: ")
                pwd = input("Set a password for this encrypted file: ")
                encrypt_file(file_to_encrypt, user, pwd)
        elif choice == "2":
            root = Tk()
            root.withdraw()
            file_to_decrypt = filedialog.askopenfilename(initialdir=CRYPTED_FILES_FOLDER,
                                                         title="Select an encrypted file to decrypt")
            if file_to_decrypt:
                user = input("Enter username: ")
                pwd = input("Enter password: ")
                decrypt_file(file_to_decrypt, user, pwd)
        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


# Main function
if __name__ == "__main__":
    generate_key()  # Generate encryption key
    display_ascii_art()
    if login():
        main_menu()
