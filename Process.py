import sqlite3
import hashlib

connection = sqlite3.connect("NoteBankSystem.db")
print(connection.total_changes)
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
            return [True,False]

    cursor.execute("SELECT StaffId, Password from Staff")
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == email and row[1] == password:
            return [True,True]

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




