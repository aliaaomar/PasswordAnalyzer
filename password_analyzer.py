import re
import math
import random
import string
import bcrypt
import os
import base64
import getpass
import json
import pyperclip  # For clipboard integration
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256

# 1. List of Breached Passwords
BREACHED_PASSWORDS = [
    "12345", "123456", "password", "admin", "123456789",
    "qwerty", "abc123", "password1", "letmein", "welcome",
    "monkey", "football", "iloveyou", "123123", "sunshine",
    "master", "login", "admin123", "password123"
]

# 2. Check if Password is Breached
def is_breached(password):
    return password.lower() in BREACHED_PASSWORDS

# 3. Password Evaluation
def evaluate_password(password):
    score = 0
    feedback = []

    # Check for breached passwords
    if is_breached(password):
        feedback.append("This password is commonly used or breached. Choose a different password.")
        return score, feedback

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short. Use at least 12 characters.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add at least one number.")
    
    if re.search(r'[@$!%*?&#]', password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g., @, $, etc.).")

    if re.search(r'(.)\1{2,}', password):
        feedback.append("Avoid repeated characters.")
    
    return score, feedback

# 4. Entropy Calculation
def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in '@$!%*?&#' for c in password): charset += len('@$!%*?&#')
    
    entropy = len(password) * math.log2(charset)
    return entropy

# 5. Analyze Password
def analyze_password(password):
    score, feedback = evaluate_password(password)
    entropy = calculate_entropy(password)
    
    print(f"\nPassword Score: {score}/7")
    print(f"Entropy: {entropy:.2f} bits")
    if feedback:
        print("Recommendations:")
        for tip in feedback:
            print(f"- {tip}")
        print("\nSuggested Strong Password:")
        print(generate_password(16))
    else:
        print("Your password is strong!")

# 6. Generate Password with Clipboard Integration
def generate_password(length=16):
    """
    Generate a strong random password and copy it to the clipboard.
    """
    characters = string.ascii_letters + string.digits + '@$!%*?&#'
    password = ''.join(random.choice(characters) for _ in range(length))
    pyperclip.copy(password)  # Copy to clipboard
    print(f"Generated Password: {password}")
    print("The password has been copied to the clipboard.")
    return password

# 7. Store Password with Timestamp
def store_password_in_file(name, password, master_password):
    """
    Hashes the password using bcrypt, adds a timestamp, and stores it securely in a file.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "name": name,
        "hashed_password": hashed_password,
        "timestamp": timestamp
    }
    with open("passwords_bcrypt.json", "a") as file:
        file.write(json.dumps(data) + "\n")
    print("Password stored securely!")

# 8. Retrieve Password and Check Age with Attempt Limitation
def retrieve_password_from_file(name, password):
    """
    Retrieve the hashed password from the file, verify it, check its age, and limit brute force attempts.
    """
    max_attempts = 3  # Maximum number of attempts allowed
    attempts = 0  # Initialize attempts counter

    try:
        with open("passwords_bcrypt.json", "r") as file:
            for line in file:
                data = json.loads(line.strip())
                if data["name"] == name:
                    hashed_password = data["hashed_password"]
                    timestamp = datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S')
                    age = (datetime.now() - timestamp).days

                    # Suggest changing the password if older than 90 days
                    if age > 90:
                        print(f"Warning: The password for '{name}' is {age} days old. Consider changing it.")

                    # Attempt password verification
                    while attempts < max_attempts:
                        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                            print("Password verified successfully!")
                            return
                        else:
                            attempts += 1
                            if attempts < max_attempts:
                                password = getpass.getpass("Incorrect password. Try again: ")
                            else:
                                print("Maximum attempts reached. Access denied.")
                                return
        print("Password not found!")
    except Exception as e:
        print(f"Error: {e}")

# 9. Help Menu
def display_help():
    print("\n=== Help Menu ===")
    print("1. Generate a Strong Password: Creates a secure random password.")
    print("2. Analyze a Password: Evaluates a password's strength and entropy.")
    print("3. Store a Password Securely: Hashes and stores a password in a file.")
    print("4. Retrieve a Stored Password: Verifies a password and checks its age.")
    print("5. Help: Shows this guide.")
    print("6. Exit: Exits the program.\n")

# 10. Main Menu-Based Interface
def main():
    while True:
        print("\n=== Secure Command-Line Password Strength Analyzer ===")
        print("1. Generate a Strong Password")
        print("2. Analyze a Password")
        print("3. Store a Password Securely")
        print("4. Retrieve a Stored Password")
        print("5. Help")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            length = int(input("Enter the desired password length (default 16): ") or 16)
            generate_password(length)

        elif choice == '2':
            password = getpass.getpass("Enter the password to analyze: ")
            analyze_password(password)

        elif choice == '3':
            name = input("Enter a name for the password (e.g., 'email', 'bank'): ")
            password = getpass.getpass("Enter the password to store: ")
            master_password = getpass.getpass("Enter a master password: ")
            store_password_in_file(name, password, master_password)

        elif choice == '4':
            name = input("Enter the name of the password to retrieve: ")
            password = getpass.getpass("Enter the password to verify: ")
            retrieve_password_from_file(name, password)

        elif choice == '5':
            display_help()

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




