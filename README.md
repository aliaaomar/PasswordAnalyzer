# Secure Command-Line Password Strength Analyzer & Vault

A command-line cybersecurity tool developed in Python to evaluate credential hygiene, quantify password entropy, generate cryptographically secure passwords, and store credentials safely using local encryption and robust hashing mechanisms.

---

## Key Features

### 1. Cryptographic Password Generation
* Dynamically generates high-entropy strings utilizing characters across diverse pools (lowercase, uppercase, digits, and special characters).
* Supports custom length specifications (defaults to 16 characters).
* Automatically copies newly generated passwords to the system clipboard to prevent shoulder-surfing and terminal leakage.

### 2. Comprehensive Password Strength & Entropy Analysis
* **Shannon Entropy Calculation:** Measures the mathematical unpredictability and information density of the password in bits.
* **Rule-Based Auditing (Score 1/7):** Validates length thresholds, character class diversity, and common weak patterns.
* **Actionable Feedback:** Generates clear remediation suggestions alongside an instantly recommended secure alternative.

### 3. Encrypted Local Credential Storage
* Stores password records under user-defined labels (e.g., `git`, `email`, `bank`).
* Employs **bcrypt** for slow, salted one-way hashing to protect stored credentials against offline rainbow table and dictionary attacks.
* Secures local storage vaults (`passwords.enc` / `passwords_bcrypt.json`) behind a master password mechanism.

### 4. Verification & Retrieval
* Authenticates saved credentials against stored hashes.
* Verifies password validity and monitors credential usage safely from the terminal.

---

## Security & Architecture Considerations

* **Clipboard Safety:** Utilizes `pyperclip` to streamline handling credentials directly into target applications without writing plaintext secrets to shell history logs.
* **Defensive Storage:** Vault records and hash databases are kept strictly local. Pre-configured `.gitignore` directives ensure local stores (`*.enc`, `*.json`) are never tracked or committed to version control.
* **Salting & Key Derivation:** Leverages modern key-stretching via bcrypt to mitigate rapid brute-force computations.

---

## Installation & Setup

### Prerequisites
* Python 3.8+
* `git` installed on your machine

### 1. Clone the Repository
```bash
git clone [https://github.com/aliaaomar/PasswordAnalyzer.git](https://github.com/aliaaomar/PasswordAnalyzer.git)
cd PasswordAnalyzer
```

### 2. Install Required Dependencies
```bash
pip install pyperclip bcrypt cryptography
```

*(Alternatively, run `pip install -r requirements.txt` if using a requirements manifest).*

---

## Usage

Run the tool directly from PowerShell, Command Prompt, or any Unix-like terminal:

```bash
python password_analyzer.py
```

### Menu Interface
```text
=== Secure Command-Line Password Strength Analyzer ===
1. Generate a Strong Password
2. Analyze a Password
3. Store a Password Securely
4. Retrieve a Stored Password
5. Help
6. Exit
```

---

## Project Structure

```text
PasswordAnalyzer/
├── .gitignore               # Excludes virtual environments and sensitive credential databases
├── password_analyzer.py     # Main application logic (CLI, entropy engine, storage)
└── README.md                # Project documentation and specifications
```

