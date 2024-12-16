from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Frame, ttk
import Process

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Admin\Desktop\AdData\NoteBank\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def validation(entry1, entry2):
    """Validate user credentials and switch to the home page if correct."""
    log = Process.signin(entry1, entry2)
    print(f"Log: {log}")
    if log[0] == True and log[1] == False:
        switch_to_home_page()
    elif log[0] == True and log[1] == True:
        switch_to_home_page() #if both are true it's a staff account
    elif not log[0]:
        error_label0.config(text="Invalid email or password", fg="red")

def account_creation_validation(firstname, lastname, dob, email, address, work,
                   branch, password):
    log = Process.create_account(firstname, lastname, dob, email, address, work,
                   branch, password)
    if log:
        error_label1.config(text="", fg="red")
        switch_to_login_page()
    else:
        error_label1.config(text="Please type correctly the data and select a valid branch\n"
                                "First Name, Last Name, Branch, Email, and Password are required!", fg="red")


def forgot_password_validation(firstname, lastname, password, email, address, work, combobox):
    loge = Process.reset_password(firstname, lastname, password, email, address, work, combobox)
    if loge[0] == True and loge[1] == False:
        error_label.config(text="", fg="red")
        switch_to_login_page()
    elif not loge[0] and loge[1] == True:
        error_label.config(text="All fields are required.", fg="red")
    elif not loge[0] and loge[1] == False:
        error_label.config(text="There is no account associated with this email.", fg="red")
    elif loge[0] == True and loge[1] == True:
        error_label.config(text="Your verification credentials do not match \n the one of the account", fg="red")

def switch_to_home_page():
    """Switch to the home page."""
    login_frame.pack_forget()
    create_account_frame.forget()
    home_frame.pack(fill="both", expand=True)

def switch_to_login_page():
    """Switch back to the login page."""
    home_frame.pack_forget()
    create_account_frame.forget()
    #forgot_password_frame.forget()
    entry_1.delete(0, 'end')
    entry_2.delete(0, 'end')
    login_frame.pack(fill="both", expand=True)
    login_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

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
      # Clear the create account fields before switching
    login_frame.pack_forget()
    forgot_password_frame.pack(fill="both", expand=True)

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

# Home Frame
home_frame = Frame(window, bg="#E7E8D1")
Label(
    home_frame,
    text="Welcome to the Home Page!",
    bg="#E7E8D1",
    fg="#B85042",
    font=("Inter SemiBold", 24)
).pack(pady=50)

Button(
    home_frame,
    text="Log Out",
    command=switch_to_login_page,
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
).pack(pady=20)

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
entry_firstnam = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_firstnam.place(x=200.0, y=100.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 160.0, anchor="nw", text="Last Name", fill="#000000", font=("Inter", 12 * -1))
entry_lastnam = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_lastnam.place(x=200.0, y=160.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 220.0, anchor="nw", text="Date of Birth", fill="#000000", font=("Inter", 12 * -1))
entry_do = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_do.place(x=200.0, y=220.0, width=210.0, height=33.0)

canvas_create.create_text(100.0, 280.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 12 * -1))
entry_emai = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_emai.place(x=200.0, y=280.0, width=210.0, height=33.0)

# Right Column Inputs (add some space to avoid being too close to the border)
canvas_create.create_text(600.0, 100.0, anchor="nw", text="Address", fill="#000000", font=("Inter", 12 * -1))
entry_addres = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_addres.place(x=700.0, y=100.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 160.0, anchor="nw", text="Work Type", fill="#000000", font=("Inter", 12 * -1))
entry_worktyp = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_worktyp.place(x=700.0, y=160.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 220.0, anchor="nw", text="Branch", fill="#000000", font=("Inter", 12 * -1))

# Load the branches into the combobox
branches = Process.load_branches()
branch_combobo = ttk.Combobox(create_account_frame, values=branches)
branch_combobo.place(x=700.0, y=220.0, width=160.0, height=33.0)

canvas_create.create_text(600.0, 280.0, anchor="nw", text="Password", fill="#000000", font=("Inter", 12 * -1))
entry_passwor = Entry(create_account_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
entry_passwor.place(x=700.0, y=280.0, width=160.0, height=33.0)

error_label1 = Label(create_account_frame, text="", bg="#E7E8D1", fg="red", font=("Inter", 10))
error_label1.place(x=250, y=400)

submit_button = Button(
    create_account_frame,
    text="Submit",
    command=lambda: account_creation_validation(entry_firstnam, entry_lastnam, entry_do, entry_emai, entry_addres, entry_worktyp, branch_combobo, entry_passwor),
    bg="#B85042",
    fg="white",
    font=("Inter", 12),
    relief="flat"
)
submit_button.place(x=370.0, y=350.0, width=210.0, height=40.0)


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


#-----------------------------------------------------------------------------------------------
# Run the application
window.resizable(False, False)
window.mainloop()