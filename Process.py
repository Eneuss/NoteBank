import sqlite3
import hashlib
from datetime import datetime


connection = sqlite3.connect("NoteBankSystem.db")
cursor = connection.cursor()


# the function is used to hash the data of the users so it is protected in case of a steal
def hashdata(data):
    """to provide more security since the hash it's a one way only encryption we will use a technique called
        salt where some predefined characters are added to the string that we hash to prevent brute force attacks"""
    data = "!£" + data
    data_bytes = data.encode('utf-8')


    sha256 = hashlib.sha256()
    sha256.update(data_bytes)

    string_hash = sha256.hexdigest()


    return string_hash


def signin(email_entry, password_entry):
    """Validate user credentials."""
    cursor.execute("SELECT UserId, Email, Password from Users")
    rows = cursor.fetchall()
    email = email_entry.get()
    password = password_entry.get()
    if not email and not password:
        return [False]

    email = hashdata(email)
    password = hashdata(password)

    for row in rows:
        if row[1] == email and row[2] == password:
            return [True,row[0]]

    return [False]


def create_account(entry_firstname, entry_lastname, entry_dob, entry_email, entry_address, entry_worktype,
                   EntryBranch, entry_password):
    """Create an account in the database."""
    # You can add validation here as per your requirements.
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    dob = entry_dob.get()
    email = entry_email.get()
    address = entry_address.get()
    work = entry_worktype.get()
    branch = EntryBranch.get()
    password = entry_password.get()
    # We check if the user types a branch instead of selecting one of the correct ones
    tBranch = load_branches()

    if branch not in tBranch:
        return False
    else:
        cursor.execute("SELECT BranchID FROM Branches WHERE BranchName = ?", (branch,))
        result = cursor.fetchone()

    if not (firstname and lastname and branch and email and password):
        return False

    # Insert the data into the table
    cursor.execute('''INSERT INTO Users (FirstName, LastName, DOB, Email, Address, WorkType, BranchID, Password)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (hashdata(firstname), hashdata(lastname), dob, hashdata(email), hashdata(address), hashdata(work), result[0], hashdata(password)))

    connection.commit()



    return True  # After account is created we return to the login page


def load_branches():
    #Load available branches from the database to the combobox

    cursor.execute("SELECT BranchName FROM Branches")
    branches = [row[0] for row in cursor.fetchall()]

    return branches


def reset_password(entry_firstname, entry_lastname,entry_password, entry_email, entry_address,
                   entry_work, branch_combobox):
    #Reset password using the provided information
    # Get the values from the entries
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    new_password = entry_password.get()
    email = entry_email.get()
    address = entry_address.get()
    work = entry_work.get()
    branch = branch_combobox.get()

    tBranch = load_branches()
    if branch not in tBranch:
        log = [True, False]
        return log
    else:
        cursor.execute("SELECT BranchID FROM Branches WHERE BranchName = ?", (branch,))
        result = cursor.fetchone()

    cursor.execute("SELECT * FROM Users WHERE Email = ?", (hashdata(email),))
    emailCheck = cursor.fetchone()

    if not emailCheck:
        log = [False,False]
        return log  # Email dose not exists in the database

    # Validate fields (similar to Create Account)
    if (not firstname) or (not lastname) or (not email) or (not address) or (not work) or (not result):
        log = [False, True]
        return log

    # Check if the email exists in the database and match other details
    cursor.execute("""
        SELECT * FROM Users 
        WHERE Email = ? AND FirstName = ? AND LastName = ? AND Address = ? AND WorkType = ? AND BranchID = (
            SELECT BranchID FROM Branches WHERE BranchName = ?
        )
    """, (hashdata(email), hashdata(firstname), hashdata(lastname), hashdata(address), hashdata(work), branch))

    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE Users SET Password = ? WHERE Email = ?", (hashdata(new_password), hashdata(email)))
        cursor.connection.commit()
        log = [True, False]
        return log
    else:
        log = [True, True]
        return log



def balance(user):
    cursor.execute("SELECT Balance, IBAN FROM Accounts WHERE UserID = ?", (user,))
    emailCheck = cursor.fetchone()

    return emailCheck


def top_up(quantity,user):
    query = "UPDATE Accounts SET Balance = Balance + ? WHERE UserId = ?"
    cursor.execute(query, (float(quantity), user))
    connection.commit()



def insert_file_and_convert_to_blob(file_path, current_user):
    if file_path:
        try:
            # Open the image file in binary mode
            with open(file_path, 'rb') as file:
                img_data = file.read()

            # Insert the BLOB data into the database
            cursor.execute("UPDATE Accounts SET Image = ? WHERE UserId = ?", (img_data, current_user))
            connection.commit()

            print("File successfully converted to BLOB and inserted into the database.")

        except Exception as e:
            print(f"Error: {e}")


def download_file(file_id):
    #Handles file download
    try:
        cursor.execute("SELECT image FROM Accounts WHERE UserId = ?", (file_id,))
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
    # Handles file upload
    if file_path:
        try:
            insert_file_and_convert_to_blob(file_path, user)
            print("File uploaded successfully!")
        except Exception as e:
            print(f"Failed to upload the file: {e}")


def update_account(current_user, entry_firstname, entry_lastname, entry_dob, entry_email, entry_address,
                   entry_work, branch_combobox, entry_password):
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

        # If there are fields to update, execute the query
        if updates:
            update_query = f"UPDATE Users SET {', '.join(updates)} WHERE UserId = ?"
            params.append(current_user)
            cursor.execute(update_query, tuple(params))
            cursor.connection.commit()
            return True



def transaction(user, entry_recipient, entry_amount, entry_description, entry_date):
    recipient = entry_recipient.get()
    amount = entry_amount.get()
    description = entry_description.get()
    date = entry_date.get()

    if not recipient or not amount or not date:
        log = 1
        return log

    # Validate date format

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        log = 2
        return log

    amount = float(amount)
    Balance = balance(user)
    if amount > float(Balance[0]):
        print("The amount is too much ",amount)
        log = 3
        return log

    Balance = float(Balance[0]) - amount
    print(f"This is the balance {Balance}")
    query = """
            INSERT INTO Transactions (AccountId, Amount, Recipient, Description, Date)
            VALUES (?, ?, ?, ?, ?)
            """
    # Execute the query
    cursor.execute(query, (user, amount, recipient, description, date))
    connection.commit()

    cursor.execute("UPDATE Accounts SET Balance = ? WHERE AccountId = ?", (Balance, user))
    connection.commit()
    log = 5
    return log



def list_transactions():

    # Get the current year
    current_year = datetime.now().year
    # Query to retrieve transactions of the current year
    query = """
        SELECT strftime('%Y-%m', Date) AS Month, SUM(Amount) AS TotalAmount
        FROM Transactions
        WHERE strftime('%Y', Date) = ?
        GROUP BY strftime('%Y-%m', Date)
        ORDER BY Month
    """
    cursor.execute(query, (str(current_year),))
    transactions = cursor.fetchall()
    print(transactions)
    return transactions