from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Frame, ttk, Text, filedialog
import Process
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Define the assets path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    """Returns the path to assets."""
    return ASSETS_PATH / Path(path)

# Global variable to store the current user's ID
current_user = 0

def validation(entry1, entry2):
    """Validate user credentials and switch to the home page if correct."""
    log = Process.signin(entry1, entry2)
    if log[0]:
        global current_user
        current_user = log[1]
        switch_to_home_page()
    else:
        error_label0.config(text="Invalid email or password", fg="red")

def account_creation_validation(firstname, lastname, dob, email, address, work, branch, password):
    """Validate and create a new account."""
    log = Process.create_account(firstname, lastname, dob, email, address, work, branch, password)
    if log:
        error_label1.config(text="", fg="red")
        switch_to_login_page()
    else:
        error_label1.config(
            text="Please type correctly the data and select a valid branch\n"
                 "First Name, Last Name, Branch, Email, and Password are required!",
            fg="red"
        )

def update_account_validation(user, firstname, lastname, dob, email, address, work, combobox, password):
    """Validate and update account details."""
    log = Process.update_account(user, firstname, lastname, dob, email, address, work, combobox, password)
    if log:
        switch_to_home_page()
    else:
        error_label4.config(text="The branch does not exist", fg="red")

def switch_to_login_page():
    """Switch back to the login page."""
    error_label.config(text="", fg="red")
    error_label0.config(text="", fg="red")
    home_frame.pack_forget()
    profile_frame.pack_forget()
    send_frame.pack_forget()
    create_account_frame.forget()
    forgot_password_frame.forget()
    entry_1.delete(0, 'end')
    entry_2.delete(0, 'end')
    login_frame.pack(fill="both", expand=True)
    login_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

def forgot_password_validation(firstname, lastname, password, email, address, work, combobox):
    """Validate and reset the user's password."""
    loge = Process.reset_password(firstname, lastname, password, email, address, work, combobox)
    if loge[0] and not loge[1]:
        error_label.config(text="", fg="red")
        switch_to_login_page()
    elif not loge[0] and loge[1]:
        error_label.config(text="All fields are required.", fg="red")
    elif not loge[0] and not loge[1]:
        error_label.config(text="There is no account associated with this email.", fg="red")
    else:
        error_label.config(
            text="Your verification credentials do not match\n the one of the account",
            fg="red"
        )

def handle_upload():
    """Handle file upload by the user."""
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif"), ("All Files", "*.*")]
    )
    Process.upload_file(file_path, current_user)

def handle_download():
    """Handle file download by the user."""
    file_data = Process.download_file(current_user)
    if file_data:
        save_path = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".jpg",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif"), ("All Files", "*.*")]
        )
        if save_path:
            with open(save_path, 'wb') as file:
                file.write(file_data)
            print(f"File saved to: {save_path}")
        else:
            print("Save operation canceled.")
    else:
        print("No file to save.")

def send_validation(current_user, recipient, amount, description, date):
    """Validate and process a transaction."""
    log = Process.transaction(current_user, recipient, amount, description, date)
    if log == 1:
        error_label5.config(text="Fill all the required data", fg="red")
    elif log == 2:
        error_label5.config(text="Error: Date must be in YYYY-MM-DD format and a valid date.", fg="red")
    elif log == 3:
        error_label5.config(text="Error: Amount must be a valid number.", fg="red")
    else:
        switch_to_home_page()

def update_balance():
    """Fetch and display the current balance."""
    current_balance = Process.balance(current_user)
    canvas.itemconfig(balance_text, text=f"{current_balance[0]}£")
    canvas.itemconfig(iban, text=f"IBAN: {current_balance[1]}")

def create_plot(transactions):
    """Create and display a plot for transactions."""
    months = [transaction[0] for transaction in transactions]
    amounts = [transaction[1] for transaction in transactions]

    # Create a smaller plot (adjusted size)
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.bar(months, amounts, color='skyblue')
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount")
    ax.set_title("Total Transactions per Month")

    # Embed the plot below the Iban label (adjust the position)
    canvas_plot = FigureCanvasTkAgg(fig, master=home_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().place(x=100, y=200)


def export_transactions_to_xml():
    """
    Handle exporting transactions for the current user to XML.
    """
    root = Process.export_transactions(current_user)

    # Prompt the user to save the file
    save_path = filedialog.asksaveasfilename(
        title="Save Transactions as XML",
        defaultextension=".xml",
        filetypes=[("XML Files", "*.xml")]
    )
    if save_path:
        tree = ET.ElementTree(root)
        tree.write(save_path, encoding="utf-8", xml_declaration=True)
        print(f"Transactions exported to {save_path}")

def import_transactions_from_xml():
    """
    Handle importing transactions from an XML file.
    """
    # Prompt the user to open a file
    file_path = filedialog.askopenfilename(
        title="Open Transactions XML File",
        filetypes=[("XML Files", "*.xml")]
    )
    if file_path:
        success = Process.import_transactions_from_xml(file_path)
        if success:
            print("Transactions imported successfully.")
        else:
            print("Failed to import transactions.")


def switch_to_home_page():
    """Switch to the home page."""
    profile_frame.pack_forget()
    send_frame.pack_forget()
    update_balance()
    login_frame.pack_forget()
    create_account_frame.forget()
    branch_combobo.set("")
    home_frame.pack(fill="both", expand=True)

def switch_to_create_account_page():
    """Switch to the create account page."""
    login_frame.pack_forget()
    home_frame.pack_forget()
    entry_firstnam.delete(0, 'end')
    entry_lastnam.delete(0, 'end')
    entry_do.delete(0, 'end')
    entry_emai.delete(0, 'end')
    entry_addres.delete(0, 'end')
    entry_worktyp.delete(0, 'end')
    entry_passwor.delete(0, 'end')
    create_account_frame.pack(fill="both", expand=True)

def switch_to_forgot_password():
    """Clear the create account fields before switching to forgot password page."""
    login_frame.pack_forget()
    forgot_password_frame.pack(fill="both", expand=True)

def switch_to_profile_page():
    """Switch to the profile page."""
    home_frame.pack_forget()
    send_frame.pack_forget()
    entry_firstnam.delete(0, 'end')
    entry_lastnam.delete(0, 'end')
    entry_do.delete(0, 'end')
    entry_emai.delete(0, 'end')
    entry_addres.delete(0, 'end')
    entry_worktyp.delete(0, 'end')
    entry_passwor.delete(0, 'end')
    profile_frame.pack(fill="both", expand=True)

def switch_to_send_page():
    """Switch to the send money page."""
    home_frame.pack_forget()
    profile_frame.pack_forget()
    entry_recipient.delete(0, 'end')
    entry_amount.delete(0, 'end')
    entry_description.delete(0, 'end')
    entry_date.delete(0, 'end')
    send_frame.pack(fill="both", expand=True)

def show_top_up_form():
    """Create the top-up form for adding funds."""
    top_up_frame = Frame(home_frame, bg="#D7DEC8", width=300, height=150)
    top_up_frame.place(x=400, y=20)  # Position the form on the screen

    # Label for amount to top up
    amount_label = Label(top_up_frame, text="Amount to top up:", bg="#D7DEC8", font=("Inter", 12))
    amount_label.pack(pady=10)

    # Entry field to input the top-up amount
    quantity = Entry(top_up_frame, font=("Inter", 12))
    quantity.pack(pady=5)

    # Function to handle the confirm button click
    def confirm_top_up():
        amount = quantity.get()
        if amount.isdigit() and float(amount) > 0:
            Process.top_up(amount, current_user)
            top_up_frame.destroy()  # Close the top-up form
            switch_to_home_page()

    # Confirm button
    confirm_button = Button(
        top_up_frame,
        text="Confirm",
        bg="#B85042",
        fg="white",
        font=("Inter", 12),
        relief="flat",
        command=confirm_top_up
    )
    confirm_button.pack(pady=10)



# Main window
window = Tk()
window.geometry("900x600")
window.configure(bg="#A7BEAE")

#---------------------------------------------------
# Login Frame
login_frame = Frame(window, bg="#A7BEAE")
login_frame.pack(fill="both", expand=True)
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)  # Centered within the 900x600 window

canvas = Canvas(
    login_frame,
    bg="#A7BEAE",
    height=500,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=-10)
canvas.create_rectangle(300.0, 0.0, 600.0, 500.0, fill="#E7E8D1", outline="")
canvas.create_text(400.0, 40.0, anchor="nw", text="NoteBank", fill="#B85042", font=("Inter SemiBold", 24 * -1))

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(150.0, 250.0, image=image_image_1)

canvas.create_text(340.0, 100.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 16 * -1))
entry_1 = Entry(login_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=345.0, y=126.0, width=210.0, height=33.0)

canvas.create_text(340.0, 178.0, anchor="nw", text="Password", fill="#000000", font=("Inter", 16 * -1))
entry_2 = Entry(login_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
entry_2.place(x=345.0, y=205.0, width=210.0, height=33.0)

error_label0 = Label(login_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label0.place(x=345, y=250)

button_1 = Button(
    login_frame,
    text="Sign In",
    command=lambda: validation(entry_1, entry_2),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
button_1.place(x=340.0, y=300.0, width=100.0, height=40.0)

button_2 = Button(
    login_frame,
    text="Create Account",
    command=lambda: switch_to_create_account_page(),
    bg="#A7BEAE",
    fg="#000000",
    font=("Inter", 12),
    relief="flat"
)
button_2.place(x=450.0, y=300.0, width=130.0, height=40.0)

button_3 = Button(
    login_frame,
    text="Forgot Password",
    command=lambda: switch_to_forgot_password(),
    bg="#E7E8D1",
    fg="#000000",
    font=("Inter", 12),
    relief="flat"
)
button_3.place(x=360.0, y=370.0, width=180.0, height=30.0)
#-------------------------------------------------------------------------

home_frame = Frame(window, bg="#D7DEC8")
home_frame.pack(fill="both", expand=True)
home_frame.pack_forget()

canvas = Canvas(
    home_frame,
    bg="#D7DEC8",
    height=600,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# "Your current balance is" label
canvas.create_text(
    125.0,
    11.0,
    anchor="nw",
    text="Your current balance is :",
    fill="#000000",
    font=("Inter", 20 * -1)
)

# Display balance
balance_text = canvas.create_text(
    180.0,
    41.0,
    anchor="nw",
    text="Loading error",
    fill="#000000",
    font=("Inter", 36 * -1)
)

iban = canvas.create_text(
    125.0,
    160.0,
    anchor="nw",
    text="Iban",
    fill="#000000",
    font=("Inter", 20 * -1)
)

# "Top up" and "Send" buttons
canvas.create_rectangle(
    176.0,
    107.0,
    254.0,
    138.0,
    fill="#B85042",
    outline=""
)
canvas.create_rectangle(
    265.0,
    107.0,
    344.0,
    138.0,
    fill="#B85042",
    outline=""
)

# "Top up" and "Send" buttons
Button(
    home_frame,
    text="Top up",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 12),
    relief="flat",
    command=show_top_up_form  # Show the top-up form when clicked
).place(x=176.0, y=107.0, width=78.0, height=31.0)

Button(
    home_frame,
    text="Send",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 12),
    relief="flat",
    command=lambda: switch_to_send_page()
).place(x=265.0, y=107.0, width=79.0, height=31.0)

# Left Sidebar - Home, Profile, Cards, Loans, etc.
sidebar_frame = Frame(home_frame, bg="#B85042", width=90, height=600)
sidebar_frame.place(x=0, y=0)

Button(
        sidebar_frame,
        text="Home",
        bg="#B85042",
        fg="#E7E8D1",
        font=("Inter", 14),
        relief="flat",
        command=lambda:switch_to_home_page()
    ).place(x=0, y=19, width=90, height=40)

Button(
        sidebar_frame,
        text="Profile",
        bg="#B85042",
        fg="#E7E8D1",
        font=("Inter", 14),
        relief="flat",
        command=lambda:switch_to_profile_page()
    ).place(x=0, y=93, width=90, height=40)

Button(
        sidebar_frame,
        text="Send",
        bg="#B85042",
        fg="#E7E8D1",
        font=("Inter", 14),
        relief="flat",
        command=lambda:switch_to_send_page()
    ).place(x=0, y=167, width=90, height=40)


Button(
        sidebar_frame,
        text="Log out",
        bg="#B85042",
        fg="#E7E8D1",
        font=("Inter", 14),
        relief="flat",
        command=lambda:switch_to_login_page()
    ).place(x=0, y=533, width=90, height=40)

# "NoteBank" text at the top
canvas.create_text(
    750.0,
    33.0,
    anchor="nw",
    text="NoteBank",
    fill="#B85042",
    font=("Inter SemiBold", 24 * -1)
)
transaction = Process.list_transactions()
# Call the function to display the table and plot
create_plot(transaction)

# Right Side - Help Text Area
canvas.create_rectangle(
    700.0,
    97.0,
    900.0,
    600.0,
    fill="#B85042",
    outline=""
)

canvas.create_text(
    718.0,
    109.0,
    anchor="nw",
    text="Send a request for any\nhelp or questions to\nour staff",
    fill="#FFFFFF",
    font=("Inter SemiBold", 16 * -1)
)

# Textbox for request input
request_input = Text(
    home_frame,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    wrap="word",         # Automatically wrap text at word boundaries
    font=("Inter", 12)   # Adjust font size if needed
)
request_input.place(x=725.0, y=189.0, width=155.0, height=307.0)


request_input.insert("1.0", "")  # Start text from the top-left

# Submit Button for request
submit_button = Button(
    home_frame,
    text="Submit",
    command=lambda: switch_to_home_page(),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
submit_button.place(x=725.0, y=530.0, width=155.0, height=40.0)



#Now there will be the frame of the create account
#------------------------------------------------------------------------------

create_account_frame = Frame(window, bg="#E7E8D1")

canvas_create = Canvas(
    create_account_frame,
    bg="#E7E8D1",
    height=600,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas_create.place(x=0, y=0)

canvas_create.create_text(400.0, 40.0, anchor="nw", text="Create Account", fill="#B85042", font=("Inter SemiBold", 24))

# Left Column Inputs
canvas_create.create_text(100.0, 100.0, anchor="nw", text="First Name", fill="#000000", font=("Inter", 12 * -1))
entry_firstn = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_firstn.place(x=200.0, y=100.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 160.0, anchor="nw", text="Last Name", fill="#000000", font=("Inter", 12 * -1))
entry_lastn = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_lastn.place(x=200.0, y=160.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 220.0, anchor="nw", text="Date of Birth", fill="#000000", font=("Inter", 12 * -1))
entry_d = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_d.place(x=200.0, y=220.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 280.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 12 * -1))
entry_em = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_em.place(x=200.0, y=280.0, width=210.0, height=33.0)

# Right Column Inputs (add some space to avoid being too close to the border)
canvas_create.create_text(600.0, 100.0, anchor="nw", text="Address", fill="#000000", font=("Inter", 12 * -1))
entry_addr = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_addr.place(x=700.0, y=100.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 160.0, anchor="nw", text="Work Type", fill="#000000", font=("Inter", 12 * -1))
entry_workt = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_workt.place(x=700.0, y=160.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 220.0, anchor="nw", text="Branch", fill="#000000", font=("Inter", 12 * -1))

# Load the branches into the combobox
branches = Process.load_branches()
branch_comb = ttk.Combobox(create_account_frame, values=branches)
branch_comb.place(x=700.0, y=220.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 280.0, anchor="nw", text="Password", fill="#000000", font=("Inter", 12 * -1))
entry_passw = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
entry_passw.place(x=700.0, y=280.0, width=160.0, height=33.0)


error_label1 = Label(create_account_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label1.place(x=250, y=460)

submit_button = Button(
    create_account_frame,
    text="Submit",
    command=lambda: account_creation_validation(entry_firstn, entry_lastn, entry_d, entry_em, entry_addr, entry_workt, branch_comb, entry_passw),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
submit_button.place(x=370.0, y=400.0, width=210.0, height=40.0)


#---------------------------------------------------------------------------------------------
forgot_password_frame = Frame(window, bg="#E7E8D1")
forgot_password_frame.pack_forget()

canvas_forgot_password = Canvas(
    forgot_password_frame,
    bg="#E7E8D1",
    height=600,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas_forgot_password.place(x=0, y=0)
canvas_forgot_password.create_rectangle(0.0, 0.0, 900.0, 600.0, fill="#E7E8D1", outline="")
canvas_forgot_password.create_text(400.0, 40.0, anchor="nw", text="Reset Password", fill="#B85042", font=("Inter SemiBold", 24 * -1))

# First Name
canvas_forgot_password.create_text(150.0, 100.0, anchor="nw", text="First Name", fill="#000000", font=("Inter", 12 * -1))
entry_firstname = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_firstname.place(x=150.0, y=130.0, width=210.0, height=33.0)

# Last Name
canvas_forgot_password.create_text(150.0, 180.0, anchor="nw", text="Last Name", fill="#000000", font=("Inter", 12 * -1))
entry_lastname = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_lastname.place(x=150.0, y=210.0, width=210.0, height=33.0)

# Email
canvas_forgot_password.create_text(150.0, 260.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 12 * -1))
entry_email = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_email.place(x=150.0, y=290.0, width=210.0, height=33.0)

#Password
canvas_forgot_password.create_text(150.0, 340.0, anchor="nw", text=" New Password", fill="#000000", font=("Inter", 12 * -1))
entry_password = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_password.place(x=150.0, y=370.0, width=210.0, height=33.0)

# Address
canvas_forgot_password.create_text(450.0, 100.0, anchor="nw", text="Address", fill="#000000", font=("Inter", 12 * -1))
entry_address = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_address.place(x=450.0, y=130.0, width=210.0, height=33.0)

# Work Type
canvas_forgot_password.create_text(450.0, 180.0, anchor="nw", text="Work Type", fill="#000000", font=("Inter", 12 * -1))
entry_worktype = Entry(forgot_password_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_worktype.place(x=450.0, y=210.0, width=210.0, height=33.0)

# Branch

canvas_forgot_password.create_text(450.0, 260.0, anchor="nw", text="Select Branch", fill="#000000", font=("Inter", 12 * -1))
branches = Process.load_branches()
branch_combobox = ttk.Combobox(forgot_password_frame, values=branches)
branch_combobox.place(x=450.0, y=290.0, width=210.0, height=33.0)

# Error Label
error_label = Label(forgot_password_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label.place(x=200.0, y=400.0)

# Submit Button
submit_button = Button(
    forgot_password_frame,
    text="Submit",
    command=lambda: forgot_password_validation(entry_firstname, entry_lastname, entry_password, entry_email, entry_address,
                                               entry_worktype, branch_combobox),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
submit_button.place(x=350.0, y=450.0, width=210.0, height=40.0)
#--------------------------------------------
# Profile Frame
profile_frame = Frame(window, bg="#D7DEC8")
profile_frame.pack(fill="both", expand=True)
profile_frame.pack_forget()

# Sidebar (Left Side)
sidebar_frame_profile = Frame(profile_frame, bg="#B85042", width=90, height=600)
sidebar_frame_profile.place(x=0, y=0)

Button(
    sidebar_frame_profile,
    text="Home",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_home_page()
).place(x=0, y=19, width=90, height=40)

Button(
    sidebar_frame_profile,
    text="Profile",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_profile_page()
).place(x=0, y=93, width=90, height=40)

Button(
    sidebar_frame_profile,
    text="Send",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_send_page()
).place(x=0, y=167, width=90, height=40)


Button(
    sidebar_frame_profile,
    text="Log out",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_login_page()
).place(x=0, y=533, width=90, height=40)

# Form Section (Right Side)
form_frame = Frame(profile_frame, bg="#E7E8D1", width=810, height=600)
form_frame.place(x=90, y=0)

canvas_form = Canvas(
    form_frame,
    bg="#E7E8D1",
    height=600,
    width=810,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas_form.place(x=0, y=0)

canvas_form.create_text(250.0, 35.0, anchor="nw", text="Edit Account Details", fill="#B85042", font=("Inter SemiBold", 24))

# Left Column Inputs
canvas_form.create_text(70.0, 100.0, anchor="nw", text="First Name", fill="#000000", font=("Inter", 12 * -1))
entry_firstnam = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_firstnam.place(x=160.0, y=100.0, width=210.0, height=33.0)

canvas_form.create_text(70.0, 160.0, anchor="nw", text="Last Name", fill="#000000", font=("Inter", 12 * -1))
entry_lastnam = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_lastnam.place(x=160.0, y=160.0, width=210.0, height=33.0)

canvas_form.create_text(70.0, 220.0, anchor="nw", text="Date of Birth", fill="#000000", font=("Inter", 12 * -1))
entry_do = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_do.place(x=160.0, y=220.0, width=210.0, height=33.0)

canvas_form.create_text(70.0, 280.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 12 * -1))
entry_emai = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_emai.place(x=160.0, y=280.0, width=210.0, height=33.0)

# Right Column Inputs
canvas_form.create_text(500.0, 100.0, anchor="nw", text="Address", fill="#000000", font=("Inter", 12 * -1))
entry_addres = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_addres.place(x=600.0, y=100.0, width=160.0, height=33.0)

canvas_form.create_text(500.0, 160.0, anchor="nw", text="Work Type", fill="#000000", font=("Inter", 12 * -1))
entry_worktyp = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_worktyp.place(x=600.0, y=160.0, width=160.0, height=33.0)

canvas_form.create_text(500.0, 220.0, anchor="nw", text="Branch", fill="#000000", font=("Inter", 12 * -1))
branches = Process.load_branches()
branch_combobo = ttk.Combobox(form_frame, values=branches)
branch_combobo.place(x=600.0, y=220.0, width=160.0, height=33.0)

canvas_form.create_text(500.0, 280.0, anchor="nw", text="Password", fill="#000000", font=("Inter", 12 * -1))
entry_passwor = Entry(form_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
entry_passwor.place(x=600.0, y=280.0, width=160.0, height=33.0)

# Error Label
error_label4 = Label(form_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label4.place(x=250, y=450)


canvas_form.create_text(70.0, 350.0, anchor="nw", text="Insert an image\nof you for\nidentification", fill="#000000", font=("Inter", 12 * -1))
# Add upload and download buttons in profile_frame
upload_button = Button(
    profile_frame,
    text="Upload File",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda:handle_upload()
)
upload_button.place(x=250, y=350, width=150, height=40)

download_button = Button(
    profile_frame,
    text="Download File",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda:handle_download()
)
download_button.place(x=410, y=350, width=150, height=40)

# Submit Button
submit_button = Button(
    form_frame,
    text="Save Changes",
    command=lambda: update_account_validation(current_user, entry_firstnam, entry_lastnam, entry_do, entry_emai, entry_addres, entry_worktyp, branch_combobo, entry_passwor),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
submit_button.place(x=250.0, y=500.0, width=210.0, height=40.0)
#----------------------------------------------------------------------------------------------

# Send Frame
send_frame = Frame(window, bg="#D7DEC8")
send_frame.pack(fill="both", expand=True)
send_frame.pack_forget()

# Sidebar (Left Side)
sidebar_frame_profile = Frame(send_frame, bg="#B85042", width=90, height=600)
sidebar_frame_profile.place(x=0, y=0)

Button(
    sidebar_frame_profile,
    text="Home",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_home_page()
).place(x=0, y=19, width=90, height=40)

Button(
    sidebar_frame_profile,
    text="Profile",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_profile_page()
).place(x=0, y=93, width=90, height=40)

Button(
    sidebar_frame_profile,
    text="Send",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_send_page()
).place(x=0, y=167, width=90, height=40)


Button(
    sidebar_frame_profile,
    text="Log out",
    bg="#B85042",
    fg="#E7E8D1",
    font=("Inter", 14),
    relief="flat",
    command=lambda: switch_to_login_page()
).place(x=0, y=533, width=90, height=40)

# Main Content (Right Side)
canvas_send = Canvas(
    send_frame,
    bg="#D7DEC8",
    height=600,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas_send.place(x=90, y=0)

canvas_send.create_text(
    300.0,
    20.0,
    anchor="nw",
    text="Send Money",
    fill="#B85042",
    font=("Inter SemiBold", 24)
)

# Recipient Input
canvas_send.create_text(
    100.0,
    80.0,
    anchor="nw",
    text="Recipient",
    fill="#000000",
    font=("Inter", 12)
)
entry_recipient = Entry(send_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_recipient.place(x=350.0, y=80.0, width=400.0, height=30.0)

# Amount Input
canvas_send.create_text(
    100.0,
    140.0,
    anchor="nw",
    text="Amount (£)",
    fill="#000000",
    font=("Inter", 12)
)
entry_amount = Entry(send_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_amount.place(x=350.0, y=140.0, width=400.0, height=30.0)

# Description Input (Optional)
canvas_send.create_text(
    100.0,
    200.0,
    anchor="nw",
    text="Description (Optional)",
    fill="#000000",
    font=("Inter", 12)
)
entry_description = Entry(send_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_description.place(x=350.0, y=200.0, width=400.0, height=30.0)

# Date Display (Auto-Generated)
canvas_send.create_text(
    100.0,
    260.0,
    anchor="nw",
    text="Date (YYYY-MM-DD)",
    fill="#000000",
    font=("Inter", 12)
)
entry_date = Entry(send_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_date.place(x=350.0, y=260.0, width=200.0, height=30.0)

error_label5 = Label(send_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label5.place(x=400, y=400)


# Submit Button
submit_button = Button(
    send_frame,
    text="Submit",
    bg="#B85042",
    fg="#FFFFFF",
    font=("Inter", 14),
    relief="flat",
    command=lambda: send_validation(current_user, entry_recipient, entry_amount, entry_description, entry_date)
)
submit_button.place(x=400.0, y=320.0, width=150.0, height=40.0)

instructions_label = Label(
    send_frame,
    text="Save the list of all your transactions or import them if you need to restore your data!",
    bg="#D7DEC8",
    fg="#000000",
    font=("Inter", 12),
    wraplength=400,
    justify="center"
)
instructions_label.place(x=220, y=400, width=500, height=50)

export_button = Button(
    send_frame,
    text="Export Transactions",
    command=export_transactions_to_xml,
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
export_button.place(x=250, y=480, width=180, height=40)

import_button = Button(
    send_frame,
    text="Import Transactions",
    command=import_transactions_from_xml,
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
import_button.place(x=500, y=480, width=180, height=40)




#-----------------------------------------------------------------------------------------------
# Run the application
window.resizable(False, False)
window.mainloop()