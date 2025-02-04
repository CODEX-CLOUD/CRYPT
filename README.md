# File Encryption and Decryption Tool

## Overview

This is a Python-based tool for encrypting and decrypting files securely using the **Fernet encryption standard** from the `cryptography` library. It allows users to set unique credentials (username and password) for each encrypted file and validates these credentials before decrypting files. The project is designed with simplicity while ensuring security.

## Features

- Securely encrypt files using Fernet symmetric-key encryption.
- Decrypt files using stored credentials (username + password).
- Simple login system to control access.
- Normalized file path handling to ensure consistent operations across platforms (Windows, Linux, macOS, WSL).
- User-friendly CLI (Command Line Interface) for encrypting and decrypting files.
- Automatic encryption key generation and storage in a local file (`key.key`).
- Stores encrypted file credentials in a separate JSON-based file (`credentials.json`).
- Cross-platform compatibility.

## Requirements

- Python 3.7 or later
- `cryptography` library

## Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/CODEX-CLOUD/CRYPT
   cd PythonProject
   ```

2. **Install Dependencies**:
   Run the following command to install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t already have a `requirements.txt` file, create one with the following content:
   ```plaintext
   cryptography==41.0.0
   ```

3. **Setup Directory Structure**:
   Make sure your project directory includes the following structure:
   ```
   PythonProject/
   ├── CRYPT/
   │   ├── crypted_files/          # Folder for storing encrypted files
   ├── key.key                     # Will be generated automatically
   ├── credentials.json            # Will be created automatically
   ```

4. **Run the Program**:
   Use the script as the main entry point:
   ```bash
   sudo python3 CRYPT.py
   ```

## Usage Instructions

### 1. **Login**
   The login credentials are hard-coded for now. When prompted, enter:
   - **Username**: `admin`
   - **Password**: `password`
   
   If you fail the login, the program will exit.

### 2. **Encrypt a File**
   From the main menu, select the option to encrypt a file. Then:
   - Use the file selector dialog to pick the file you want to encrypt.
   - Provide a username and password for the encrypted file.
   - The file will be saved in the `CRYPT/crypted_files` directory with `.crypt` extension.
   - The credentials will be saved in `credentials.json`.

### 3. **Decrypt a File**
   From the main menu, select the option to decrypt a file. Then:
   - Use the file selector dialog to choose an encrypted file.
   - Input the credentials (username and password) to unlock it.
   - The decrypted file will be saved in the same directory, with `_decrypted` added to its filename.

### 4. **Exit**
   From the main menu, you can select the "Exit" option to safely close the application.

## Directory Structure

The project directory structure will look like this during operation:
```plaintext
PythonProject/
├── CRYPT/
│   ├── crypted_files/          # Contains files encrypted by the program
│       └── example.txt.crypt   # Example of an encrypted file
├── credentials.json            # Stores credentials for encrypted files
├── key.key                     # Encryption key (DO NOT SHARE THIS FILE)
├── main_script.py              # Entry point script
├── README.md                   # Project documentation (this file)
└── requirements.txt            # Python dependencies
```

## Security Notes

1. **Encryption Key**:
   - The encryption key (`key.key`) is essential to decrypt encrypted files.
   - Keep this file SAFE and DO NOT SHARE it.

2. **Credentials (`credentials.json`)**:
   - Each encrypted file is associated with unique credentials (username + password).
   - Do not expose `credentials.json` to unauthorized parties.

3. **Case Sensitivity**:
   - **Username comparisons**: Case-insensitive.
   - **Password comparisons**: Case-sensitive for additional security.

4. **Platform Considerations**:
   - Paths are automatically normalized, but you should avoid manually moving encrypted files or modifying filenames to prevent mismatches.

## Troubleshooting

1. **"File not found in credentials!"**:
   - Ensure the file path for the encrypted file matches what is stored in `credentials.json` (file paths must match exactly).
   - Do not rename or move encrypted files after processing them.

2. **"Invalid username or password!"**:
   - Verify that the credentials provided are correct.
   - Passwords are case-sensitive, but usernames are case-insensitive.

3. **"Encryption key not found"**:
   - The `key.key` file is missing. Re-run the program to regenerate it, but note that previously encrypted files won’t be recoverable without the original key.

4. **File Was Not Saved**:
   - Ensure the program has permissions to write to its directories (e.g., `CRYPT/crypted_files` for encrypted files).

## Future Improvements

- Add functionality to reset passwords or recover credentials.
- Implement graphical interface (GUI) for more user-friendly interaction.
- Use secure password hashing for storing credentials.
- Add better error reporting for edge cases.

## License

This project is open-source for educational purposes. You are free to use, modify, and share it with proper attribution.

---