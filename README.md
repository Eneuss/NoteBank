# NoteBank Application

## Description
The **NoteBank application** is a desktop banking application built using Python.  
It includes features such as:
- User account management
- Transactions handling
- XML data import/export  
The system connects to an **SQLite database** for data storage and uses **Tkinter** for the graphical user interface.

---

##  Project Structure
```
NoteBank/
├── assets/                  # Contains the image assets for the GUI
│   ├── frame0/
│       └── image_1.png      # Image used in the main program
├── database/                # Contains the SQLite database
│   └── NoteBankSystem.db
├── ExcelEntriesAndDiagram/  
│   ├── Diagram.png          # ERD Diagram structure of the database
│   ├── NoteBankEntries.xlsx # Example data entries for the database
├── main.py                  # Main application script
├── process.py               # Backend logic and database functions
├── README.md                # Documentation file
├── NoteBank_presentation.mov # Short video demo of the program
```
---

##  How to Run the Application

### **Steps to Start the Application**
1. **Navigate to the main directory** where `main.py` is located.
2. **Execute the file**:
   ```sh
   main.py
   ```
3. **Use the GUI to interact with the banking system**.

---

##  Key Features

### **User Authentication**
- Secure **login with email and password**.
- Create a new account with **encrypted credentials**.
- Reset forgotten passwords.

### **Transactions Management**
- View **current balance**.
- Perform **transactions (send money)**.
- **Top-up** account balance.

### **XML Data Handling**
- **Export** transactions to XML format for backup.
- **Import** transactions from an XML file to restore data.

### **Data Visualization**
- View **transaction summaries** with monthly totals.
- Displayed using **bar charts** with `matplotlib`.

---

##  Testing

### **Functional Tests**
- **Login Test**: Validate login credentials (valid/invalid).
- **Account Creation Test**: Create accounts with proper validation.
- **Transaction Test**: Ensure transactions work correctly with sufficient balance.

### **Integration Tests**
- Test **GUI interactions with the database** (e.g., transaction storage).
- Verify **XML import/export** functions work seamlessly.

### **Non-Functional Tests**
- **Usability**: Ensure the GUI is **intuitive and user-friendly**.
- **Security**: Validate **data encryption** (e.g., password hashing).

---

##  XML Features

### **Export Transactions**
1. **Go to the Home page** in the application.
2. Click on the **"Export Transactions"** button.
3. Choose a location and **save the transactions as an XML file**.

### **Import Transactions**
1. **Go to the Home page** in the application.
2. Click on the **"Import Transactions"** button.
3. Select an **XML file** to restore the transactions into the database.

---

##  Additional Notes
- **Database**: The SQLite database (`NoteBankSystem.db`) comes **pre-populated** with test data.
- **Dependencies**: Ensure required Python libraries are installed.
  ```sh
  pip install sqlite3 tkinter xml.etree.ElementTree matplotlib
  ```
- **Security**: Uses **password hashing** for authentication.

