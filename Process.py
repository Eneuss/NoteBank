import sqlite3
import hashlib
from datetime import datetime
import xml.etree.ElementTree as ET

connection = sqlite3.connect(r"Database\NoteBankSystem.db")
cursor = connection.cursor()

# Function to hash user data for security
def hashdata(data):
    """
    Hash user data using SHA-256 with added salt for enhanced security.
    This ensures data protection even in case of unauthorized access.
    """
    data = "!£" + data  # Add salt to the data
    data_bytes = data.encode('utf-8')  # Convert data to bytes

    sha256 = hashlib.sha256()
    sha256.update(data_bytes)  # Hash the salted data

    return sha256.hexdigest()  # Return the hexadecimal representation of the hash

def signin(email_entry, password_entry):
    """
    Validate user credentials by comparing hashed email and password.
    Returns a tuple where the first value indicates success and the second value is the user ID.
    """
    cursor.execute("SELECT UserId, Email, Password FROM Users")
    rows = cursor.fetchall()

    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:  # Check if fields are empty
        return [False]

    email = hashdata(email)  # Hash the email
    password = hashdata(password)  # Hash the password

    for row in rows:
        if row[1] == email and row[2] == password:
            return [True, row[0]]  # Return success and user ID

    return [False]  # Return failure

def create_account(entry_firstname, entry_lastname, entry_dob, entry_email, entry_address, entry_worktype, EntryBranch, entry_password):
    """
    Create a new user account in the database.
    Validates required fields and ensures the branch exists.
    """
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    dob = entry_dob.get()
    email = entry_email.get()
    address = entry_address.get()
    work = entry_worktype.get()
    branch = EntryBranch.get()
    password = entry_password.get()

    tBranch = load_branches()  # Load available branches

    if branch not in tBranch:  # Check if branch is valid
        return False
    else:
        cursor.execute("SELECT BranchID FROM Branches WHERE BranchName = ?", (branch,))
        result = cursor.fetchone()

    if not (firstname and lastname and branch and email and password):  # Check required fields
        return False

    # Insert user data into the database
    cursor.execute(
        '''INSERT INTO Users (FirstName, LastName, DOB, Email, Address, WorkType, BranchID, Password)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (hashdata(firstname), hashdata(lastname), dob, hashdata(email), hashdata(address), hashdata(work), result[0], hashdata(password))
    )
    connection.commit()
    return True  # Account creation successful

def load_branches():
    """
    Retrieve all available branches from the database.
    Returns a list of branch names.
    """
    cursor.execute("SELECT BranchName FROM Branches")
    branches = [row[0] for row in cursor.fetchall()]
    return branches

def reset_password(entry_firstname, entry_lastname, entry_password, entry_email, entry_address, entry_work, branch_combobox):
    """
    Reset a user's password if their credentials match.
    Validates all fields and checks for matching account details.
    """
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    new_password = entry_password.get()
    email = entry_email.get()
    address = entry_address.get()
    work = entry_work.get()
    branch = branch_combobox.get()

    tBranch = load_branches()
    if branch not in tBranch:
        return [True, False]

    cursor.execute("SELECT BranchID FROM Branches WHERE BranchName = ?", (branch,))
    result = cursor.fetchone()

    cursor.execute("SELECT * FROM Users WHERE Email = ?", (hashdata(email),))
    emailCheck = cursor.fetchone()

    if not emailCheck:  # Email does not exist
        return [False, False]

    # Check required fields
    if not (firstname and lastname and email and address and work and result):
        return [False, True]

    # Verify account details
    cursor.execute(
        """
        SELECT * FROM Users 
        WHERE Email = ? AND FirstName = ? AND LastName = ? AND Address = ? AND WorkType = ? AND BranchID = (
            SELECT BranchID FROM Branches WHERE BranchName = ?
        )
        """,
        (hashdata(email), hashdata(firstname), hashdata(lastname), hashdata(address), hashdata(work), branch)
    )
    user = cursor.fetchone()

    if user:  # Account details match
        cursor.execute("UPDATE Users SET Password = ? WHERE Email = ?", (hashdata(new_password), hashdata(email)))
        cursor.connection.commit()
        return [True, False]
    else:
        return [True, True]  # Verification failed

def balance(user):
    """
    Retrieve the current balance and IBAN for a given user.
    """
    cursor.execute("SELECT Balance, IBAN FROM Accounts WHERE UserID = ?", (user,))
    return cursor.fetchone()

def top_up(quantity, user):
    """
    Increase the balance of a user's account by the given amount.
    """
    query = "UPDATE Accounts SET Balance = Balance + ? WHERE UserId = ?"
    cursor.execute(query, (quantity, user))
    connection.commit()

def insert_file_and_convert_to_blob(file_path, current_user):
    """
    Insert a file as a BLOB into the database for a specific user.
    """
    if file_path:
        try:
            with open(file_path, 'rb') as file:  # Open file in binary mode
                img_data = file.read()
            cursor.execute("UPDATE Accounts SET Image = ? WHERE UserId = ?", (img_data, current_user))
            connection.commit()
            print("File successfully converted to BLOB and inserted into the database.")
        except Exception as e:
            print(f"Error: {e}")

def download_file(file_id):
    """
    Download a file (BLOB) from the database for a specific user.
    """
    try:
        cursor.execute("SELECT Image FROM Accounts WHERE UserId = ?", (file_id,))
        file_data = cursor.fetchone()
        if file_data:
            return file_data[0]  # Return binary data for the file
        else:
            print("No file found in the database.")
            return None
    except Exception as e:
        print(f"Failed to download the file: {e}")
        return None

def upload_file(file_path, user):
    """
    Handle file upload for a specific user.
    """
    if file_path:
        try:
            insert_file_and_convert_to_blob(file_path, user)
            print("File uploaded successfully!")
        except Exception as e:
            print(f"Failed to upload the file: {e}")

def update_account(current_user, entry_firstname, entry_lastname, entry_dob, entry_email, entry_address, entry_work, branch_combobox, entry_password):
    """
    Update user account details with the provided information.
    Validates all fields and updates only the provided ones.
    """
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    new_password = entry_password.get()
    email = entry_email.get()
    dob = entry_dob.get()
    address = entry_address.get()
    work = entry_work.get()
    branch = branch_combobox.get()

    tBranch = load_branches()
    if branch == "":
        result = ""
    elif branch not in tBranch:
        return False  # Invalid branch
    cursor.execute("SELECT BranchID FROM Branches WHERE BranchName = ?", (branch,))
    branch_result = cursor.fetchone()
    result = branch_result[0] if branch_result else ""

    cursor.execute("SELECT * FROM Users WHERE UserId = ?", (current_user,))
    userCheck = cursor.fetchone()

    if userCheck[0]:
        updates = []
        params = []

        if firstname:
            updates.append("FirstName = ?")
            params.append(hashdata(firstname))
        if lastname:
            updates.append("LastName = ?")
            params.append(hashdata(lastname))
        if new_password:
            updates.append("Password = ?")
            params.append(hashdata(new_password))
        if email:
            updates.append("Email = ?")
            params.append(hashdata(email))
        if dob:
            updates.append("DOB = ?")
            params.append(dob)
        if address:
            updates.append("Address = ?")
            params.append(hashdata(address))
        if work:
            updates.append("WorkType = ?")
            params.append(hashdata(work))
        if result != "":
            updates.append("BranchID = ?")
            params.append(result)

        if updates:  # Execute the query if there are updates
            update_query = f"UPDATE Users SET {', '.join(updates)} WHERE UserId = ?"
            params.append(current_user)
            cursor.execute(update_query, tuple(params))
            cursor.connection.commit()
            return True

def transaction(user, entry_recipient, entry_amount, entry_description, entry_date):
    """
    Process a transaction between two accounts.
    Validates fields and ensures sufficient balance.
    """
    recipient = entry_recipient.get()
    amount = entry_amount.get()
    description = entry_description.get()
    date = entry_date.get()

    if not recipient or not amount or not date:
        return 1  # Missing fields

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()  # Validate date format
    except ValueError:
        return 2  # Invalid date format

    amount = float(amount)
    Balance = balance(user)
    if amount > float(Balance[0]):
        print("The amount is too much ", amount)
        return 3  # Insufficient balance

    Balance = float(Balance[0]) - amount

    cursor.execute("SELECT AccountID FROM Accounts WHERE UserID = ?", (user,))
    account_id = cursor.fetchone()

    # Insert the transaction record
    query = """
        INSERT INTO Transactions (AccountId, Amount, Recipient, Description, Date)
        VALUES (?, ?, ?, ?, ?)
        """
    cursor.execute(query, (account_id[0], amount, recipient, description, date))
    connection.commit()

    # Update the account balance
    cursor.execute("UPDATE Accounts SET Balance = ? WHERE UserId = ?", (Balance, user))
    connection.commit()

    return 5  # Transaction successful

def list_transactions(user):
    """
    List all transactions for the current year, grouped by month.
    Returns a list of months and their total transaction amounts.
    """
    current_year = datetime.now().year
    print(user)
    cursor.execute("SELECT AccountID FROM Accounts WHERE UserID = ?", (user,))
    account_id = cursor.fetchone()

    query = """
        SELECT strftime('%Y-%m', Date) AS Month, SUM(Amount) AS TotalAmount
        FROM Transactions
        WHERE strftime('%Y', Date) = ? AND AccountId = ?
        GROUP BY strftime('%Y-%m', Date)
        ORDER BY Month
    """
    cursor.execute(query, (str(current_year), account_id[0]))
    transactions = cursor.fetchall()
    return transactions



def export_transactions(user_id):
    """
    Export transactions for a user to XML format.
    """
    # Fetch transactions from the database
    cursor.execute("""
            SELECT t.TransactionId, t.AccountId, t.Amount, t.Recipient, t.Description, t.Date
            FROM Transactions t
            INNER JOIN Accounts a ON t.AccountId = a.AccountID
            WHERE a.UserID = ?
        """, (user_id,))
    transactions = cursor.fetchall()

    # Create the root element
    root = ET.Element("Transactions")

    for transaction in transactions:
        transaction_element = ET.SubElement(root, "Transaction")
        ET.SubElement(transaction_element, "TransactionId").text = str(transaction[0])
        ET.SubElement(transaction_element, "AccountID").text = str(transaction[1])
        ET.SubElement(transaction_element, "Amount").text = str(transaction[2])
        ET.SubElement(transaction_element, "Recipient").text = transaction[3]
        ET.SubElement(transaction_element, "Description").text = transaction[4]
        ET.SubElement(transaction_element, "Date").text = transaction[5]

    # Return the root element for further processing
    return root

def import_transactions_from_xml(file_path):
    """
    Import transactions from an XML file into the database.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Iterate through transactions and insert them into the database
        for transaction in root.findall("Transaction"):
            account_id = transaction.find("AccountID").text
            amount = transaction.find("Amount").text
            recipient = transaction.find("Recipient").text
            description = transaction.find("Description").text
            date = transaction.find("Date").text

            print("Acc:", account_id , "AMount:", amount, "REcip: ", recipient, "Descr: ",description, "Date: ", date)
            # Insert or ignore duplicate transactions
            cursor.execute(
                "INSERT OR IGNORE INTO Transactions (AccountID, Amount, Recipient, Description, Date) VALUES (?, ?, ?, ?, ?)",
                (account_id, amount, recipient, description, date),
            )

        connection.commit()
        return True  # Success
    except Exception as e:
        print(f"Error importing transactions: {e}")
        return False  # Failure

# Function to close the connection of the database when we close the program
def closing():
    if connection:
        connection.close()
