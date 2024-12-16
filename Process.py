import sqlite3

connection = sqlite3.connect("NoteBankSystem.db")
print(connection.total_changes)
cursor = connection.cursor()


def signin(email_entry, password_entry):
    """Validate user credentials."""
    cursor.execute("SELECT UserId, Email, Password from Users")
    rows = cursor.fetchall()
    email = email_entry.get()
    password = password_entry.get()
    if not email and not password:
        return [False]
    print(f"E: {email}, P: {password}")
    for row in rows:
        if row[1] == email and row[2] == password:
            return [True,False]

    cursor.execute("SELECT StaffId, Password from Staff")
    rows = cursor.fetchall()

    for row in rows:
        if (row[0]) == int(email) and row[1] == password:
            print(row)
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
    print(f" e il nome {firstname}")
    print(firstname, lastname, email, address, work, password, branch)
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
              (firstname, lastname, dob, email, address, work, result[0], password))

    connection.commit()
    print(firstname, lastname, email, address, work, password, result)

    print("Account created successfully!")
    return True  # After account is created we return to the login page


def load_branches():
    """Load available branches from the database to the ComboBox."""

    cursor.execute("SELECT BranchName FROM Branches")
    branches = [row[0] for row in cursor.fetchall()]

    return branches


def reset_password(entry_firstname, entry_lastname,entry_password, entry_email, entry_address,
                   entry_work, branch_combobox):
    """Reset password using the provided information."""
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

    cursor.execute("SELECT 1 FROM Users WHERE Email = ?", (email,))
    emailCheck = cursor.fetchone()

    if not emailCheck:
        log = [False,False]
        return print(log)# Email dose not exists in the database

    # Validate fields (similar to Create Account)
    if not firstname or not lastname or not email or not address or not work or not result:
        log = [False, True]
        return log

    # Check if the email exists in the database and match other details (you need to implement this in your database)
    cursor.execute("""
        SELECT * FROM Users 
        WHERE Email = ? AND FirstName = ? AND LastName = ? AND Address = ? AND WorkType = ? AND BranchID = (
            SELECT BranchID FROM Branches WHERE BranchName = ?
        )
    """, (email, firstname, lastname, address, work, branch))

    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE Users SET Password = ? WHERE Email = ?", (new_password, email))
        cursor.connection.commit()
    else:
        log = [True, True]
        return log



