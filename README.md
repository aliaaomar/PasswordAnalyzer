# Secure Command-Line Password Strength Analyzer

A command-line security tool written in Python to generate cryptographically strong passwords, calculate entropy, and manage password records securely.

## Features

- **Password Generation:** Generates customizable, high-entropy passwords and copies them directly to the clipboard.
- **Strength Analysis:** Calculates Shannon entropy, assigns a score (1–7), and highlights specific security weaknesses.
- **Secure Vault:** Uses bcrypt hashing and file encryption (`passwords.enc` / `passwords_bcrypt.json`) to safely store credentials under a master password.
- **Verification:** Retrieves and verifies stored entries.

## Requirements

Ensure you have the required packages installed:
```bash
pip install pyperclip bcrypt cryptography
```

## Running the Project

```bash
python password_analyzer.py
```