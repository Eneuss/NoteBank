NoteBank Application

#Description
The NoteBank application is a desktop banking application built using Python.
It includes features such as user account management, transactions, and XML data handling for importing and exporting data.
The system connects to an SQLite database for data storage and uses Tkinter for its graphical user interface.

##Structure
```
NoteBank/
├── assets/                  # Contains the image assets for the GUI
│   ├── frame0/
│       └── image_1.png
├── database/                # Contains the SQLite database
│   └── NoteBankSystem.db
├── main.py                  # Main application script
├── process.py               # Contains backend logic and database functions
├── README.md                # Documentation

---

## How to Run the Application

# Guide to Run the Application
To start the application:
1. Navigate to the main directory where `main.py` is located.
2. Execute the main.py file
3. Navigate with the GUI to use the program

---

# Key Features
## User Authentication
- Login with email and password.
- Create a new account with necessary details.
- Reset forgotten passwords.

## Transactions Management
- View current balance.
- Perform transactions (send money).
- Top-up account balance.

## XML Data Handling
- Export transactions to XML format for backup.
- Import transactions from an XML file to restore data.

## Data Visualization
- View transaction summaries with monthly totals displayed as bar charts with python matplotlib.

---

# Testing

## Functional Tests
- **Login Test**: Test valid and invalid login credentials.
- **Account Creation Test**: Create accounts with valid and invalid data.
- **Transaction Test**: Validate successful transactions with sufficient balance.

## Integration Tests
- Test the integration between the GUI and database (e.g., transaction storage).
- Verify XML import/export functions work seamlessly with the database.

## Non-Functional Tests
- **Usability**: Ensure the GUI is intuitive and user-friendly.
- **Security**: Validate data encryption (e.g., password hashing).

---

# XML Features

## Export Transactions
- Navigate to the **Home** page and click on the "Export Transactions" button.
- Save the transactions as an XML file.

## Import Transactions
- Navigate to the **Home** page and click on the "Import Transactions" button.
- Select an XML file to restore the transactions to the database.

---
