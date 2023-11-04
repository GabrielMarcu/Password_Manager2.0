"""
First of all run Database/create_database.py

Tkinter GUI used for saving account details for any aplication the user wants.

FRAMES: login, sign_up, frame_app

global variables: user_id,  apps_l(a list of apps for a specific user_id)

Functions:

-->signup -> Used for SUBMIT button in Sign up frame. Adds new user information in database

-->login_user ->  Checks is user exists in database, and logs in the app frame

-->forgot_password -> Opens a new window used for resetting login password

-->change_password -> Resets login password, based on email from database

-->...
"""
from tkinter import *
from tkinter import messagebox, PhotoImage, ttk
import sqlite3
import password_manager as pm
import random
import string
from Database import create_database

create_database.app_db()
create_database.login_db()

# ===============================
# DATABASE CONNECTION FOR SIGN UP
# ===============================
def signup():
    """
    Used for SUBMIT button in Sign up frame.
    Adds new user information in database
    """
    if username_entry.get() == "" or emailName_entry.get() == "" or passwordName_entry.get() == "" or \
            confirm_passwordName_entry.get() == "":
        messagebox.showerror("Error", "All Fields Are Required")

    elif passwordName_entry.get() != confirm_passwordName_entry.get():
        messagebox.showerror('Error', "Password and Confirm Password Didn't Match")
    else:
        try:
            connection = sqlite3.connect("Database/password_manager.db")
            cur = connection.cursor()
            cur.execute("SELECT count(*) FROM login_table;")
            id = cur.fetchall()[0][0] + 1
            cur.execute("INSERT INTO login_table(id, username, password, email) VALUES(?,?,?,?)",
                        (id, username_entry.get(), passwordName_entry.get(), emailName_entry.get()))
            connection.commit()
            connection.close()
            clear_sign_up()
            messagebox.showinfo("Success", "New Account Created")
            show_frame(login)
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong, please try again")
            print(e)


# Clear sign up fields
def clear_sign_up():
    """
    Clears sign up entry fields
    """
    username.set("")
    email.set("")
    password.set("")
    confirm_password.set("")


# ======== DATABASE CONNECTION FOR LOGIN ==========
def login_user():
    """
    Checks is user exists in database, and logs in the app frame
    """
    try:
        global user_id
        connection = sqlite3.connect("Database/password_manager.db")
        cur = connection.cursor()

        find_user = "SELECT * FROM login_table WHERE username = ? and password = ?;"
        cur.execute(find_user, [(login_username_entry.get()), (login_password_name_entry.get())])
        result = cur.fetchall()
        if result:
            user_id = result[0][0]
            combobox_apps.config(values=app_list())
            combobox_apps.set("Pick an app")
            clear_login()
            messagebox.showinfo("Success", "Logged in Successfully")
            show_frame(frame_app)
        elif login_username_entry.get() == "" or login_password_name_entry.get() == "":
            messagebox.showerror("Warning", 'All fields are required')
        else:
            messagebox.showerror("Failed", "Incorrect username or password, pleas try again or sign up")

    except Exception as e:
        messagebox.showerror("Error", "Login failed, please Sign Up or try again")
        print(f'{e} happens after login_user')


# ======= Clear login fields ============
def clear_login():
    login_username.set("")
    login_password.set("")


# DATABASE CONNECTION FOR FORGOT PASSWORD
def forgot_password():
    """
    Opens a new window used for recovering the password
    :return: None
    """
    try:
        win = Toplevel()
        window_width = 350
        window_height = 350
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        win.title('Forgot Password')
        # win.iconbitmap('images\\aa.ico')
        win.configure(background='#272A37')
        win.resizable(False, False)

        # ====== Email ====================
        email_entry3 = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                             bd=0)
        email_entry3.place(x=40, y=80, width=256, height=50)
        email_entry3.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
        email_label3 = Label(win, text='• Email', fg="#FFFFFF", bg='#272A37',
                             font=("yu gothic ui", 11, 'bold'))
        email_label3.place(x=40, y=50)

        # ====  New Password ==================
        new_password_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), show='•',
                                   highlightthickness=1,
                                   bd=0)
        new_password_entry.place(x=40, y=180, width=256, height=50)
        new_password_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
        new_password_label = Label(win, text='• New Password', fg="#FFFFFF", bg='#272A37',
                                   font=("yu gothic ui", 11, 'bold'))
        new_password_label.place(x=40, y=150)

        # ======= Update password Button ============
        update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                             cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                             command=lambda: change_password())
        update_pass.place(x=40, y=260, width=256, height=45)
    except Exception as e:
        messagebox.showerror("Error", f"{e}, happened in forgot password frame")

    def change_password():
        try:
            if email_entry3.get == "" or new_password_entry.get() == "":
                messagebox.showerror("Error", "All Fields Are Required")
                exit_window()

            else:
                db = sqlite3.connect("./Database/password_manager.db")
                cursor = db.cursor()
                querry = "SELECT * FROM login_table WHERE email=?"
                cursor.execute(querry, [(email_entry3.get())])
                row = cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Email does not exist")
                    exit_window()
                else:
                    querry = "UPDATE login_table SET password=? where Email=?"
                    cursor.execute(querry, [new_password_entry.get(), email_entry3.get(), ])
                    db.commit()
                    db.close()
                    messagebox.showinfo("Well Done", "Password Successfully Changed")
                    exit_window()
        except Exception as e:
            print("Error", f'{e}, happened in change_password function')

    def exit_window():
        win.destroy()


def logout():
    """Logs out from application main frame and login frame is raised"""
    show_frame(login)
    listbox_details.delete(0, END)
    combobox_apps.delete(0, END)


def app_details():
    """
    Displays on a listbox login details for the selected app in the combobox, only for 1 user_id
    """
    try:
        global user_id
        listbox_details.delete(0, END)
        app_name = combobox_apps.get()
        connection = sqlite3.connect("./Database/password_manager.db")
        cursor = connection.cursor()
        details_query = "SELECT * FROM app_table WHERE user_id=? and app_name=?"
        cursor.execute(details_query, (user_id, app_name))
        details_list = cursor.fetchmany()
        listbox_details.insert(END, "APP NAME->", details_list[0][1])
        listbox_details.insert(END, "USERNAME->", details_list[0][2])
        listbox_details.insert(END, "PASSWORD->", details_list[0][3])
        listbox_details.insert(END, "EMAIL->", details_list[0][4])
    except Exception as e:
        print(f'{e} -> happened in app_details')


def app_list() -> list:
    """
    Returns a list of all application names for one user_id
    """
    try:
        global user_id
        connection = sqlite3.connect("./Database/password_manager.db")
        cursor = connection.cursor()
        find_apps = "SELECT app_name FROM app_table WHERE user_id=?"
        cursor.execute(find_apps, (str(user_id),))
        ap_list = cursor.fetchall()
        print(ap_list)
        connection.commit()
        connection.close()
        return ap_list
    except IndexError as e:
        ap_list = []
        return ap_list
    # except Exception as e:
    #     print(e, "happened in app_list function")


def random_pass_generator() -> str:
    """
    Generates a string with random characters from a string containing 8 letters, 5 digits and 3 punctuation characters
    :return: a string of 16 random characters
    """
    try:
        rand_password = random.sample(string.ascii_letters, 8) + random.sample(string.digits, 5) \
                   + random.sample(string.punctuation, 3)
        random.shuffle(rand_password)
        result = ''.join(rand_password)
        return result
    except Exception as e:
        print(f'Unexpected error: {e}')


def remove_app():
    pm.AppLoginInfo.remove_app(combobox_apps.get(), user_id)
    apps = app_list()
    combobox_apps.config(values=apps)
    combobox_apps.set("Pick an App")

def add_new_app_frame():
    """
    Opens new window used for adding new application login info into database
    """
    window = Toplevel()
    window_width = 380
    window_height = 550
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    window.title('Add new app')
    window.configure(background='#272A37')
    window.resizable(False, False)

    # =================== New App Name ====================
    new_app_entry = Entry(window, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                          bd=0, fg='#FFFFFF')
    new_app_entry.place(x=40, y=60, width=266, height=50)
    new_app_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    new_app_label = Label(window, text='• App Name', fg="#FFFFFF", bg='#272A37',
                          font=("yu gothic ui", 11, 'bold'))
    new_app_label.place(x=40, y=30)

    # ==================== New App Username =====================
    new_user_entry = Entry(window, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1, fg='#FFFFFF',
                           bd=0)
    new_user_entry.place(x=40, y=150, width=266, height=50)
    new_user_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    new_user_label = Label(window, text='• Username', fg="#FFFFFF", bg='#272A37',
                           font=("yu gothic ui", 11, 'bold'))
    new_user_label.place(x=40, y=120)

    # ===================== New App Password =====================
    new_pass_entry = Entry(window, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1, fg='#FFFFFF',
                           bd=0, show="*")
    new_pass_entry.place(x=40, y=240, width=266, height=50)
    new_pass_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    new_pass_label = Label(window, text='• Password', fg="#FFFFFF", bg='#272A37',
                           font=("yu gothic ui", 11, 'bold'))
    new_pass_label.place(x=40, y=210)

    new_confirm_pass_entry = Entry(window, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                                   fg='#FFFFFF', bd=0, show="*",
                                   )
    new_confirm_pass_entry.place(x=40, y=330, width=266, height=50)
    new_confirm_pass_label = Label(window, text='• Confirm Password', fg="#FFFFFF", bg='#272A37',
                                   font=("yu gothic ui", 11, 'bold')
                                   )
    new_confirm_pass_label.place(x=40, y=300)

    # ====================== New App Email =======================
    new_email_entry = Entry(window, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1, fg='#FFFFFF',
                            bd=0)
    new_email_entry.place(x=40, y=420, width=266, height=50)
    new_email_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    new_email_label = Label(window, text='• Email', fg="#FFFFFF", bg='#272A37',
                            font=("yu gothic ui", 11, 'bold'))
    new_email_label.place(x=40, y=390)
    # ====================== Random and Submit buttons ====================
    random_btn = Button(window, fg='#f8f8f8', text='Random', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                        cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                        command=lambda: random_btn_fnc()
                        )
    random_btn.place(x=235, y=240, width=70, height=50)

    submit_btn = Button(window, fg='#f8f8f8', text='Save', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                        cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                        command=lambda: register_new_app(new_app_entry.get(), new_user_entry.get(),
                                                         new_pass_entry.get(), new_confirm_pass_entry.get(),
                                                         new_email_entry.get())
                        )
    submit_btn.place(x=120, y=475, width=128, height=45)

    def random_btn_fnc() -> None:
        """
        Adds a random password into new password and confirm new password entries
        """
        rnd_password = random_pass_generator()
        new_pass_entry.delete(0, END)
        new_pass_entry.insert(0, rnd_password)
        new_confirm_pass_entry.delete(0, END)
        new_confirm_pass_entry.insert(0, rnd_password)

    def register_new_app(app_name: str, new_username_entry: str, password_entry: str, confirm_password_entry: str,
                         new_email: str) -> None:
        """
        Registers new application in database for one user_id
        """
        newpassword = str(password_entry)
        confirm_newpassword = str(confirm_password_entry)
        global user_id
        if app_name == "" or new_username_entry == "" or password_entry == "" or new_email == "":
            messagebox.showerror("Error", "All Fields Are Required")
        elif newpassword != confirm_newpassword:
            messagebox.showerror("Failed", "Passwords did not match")
        else:
            pm.AppLoginInfo(app_name, new_username_entry, password_entry, new_email).register_app(user_id)
            combobox_apps.config(values=app_list())
            combobox_apps.set("Pick an App")
            exit_window(window)


def update_details_window():
    """Opens a new window with the purpose of modifying login info or the selected app"""
    win = Toplevel()
    window_width = 400
    window_height = 550
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    win.title('Add new app')
    win.configure(background='#272A37')
    win.resizable(False, False)

    app_name_label = Label(win, bg="#3D404B", font=("yu gothic ui semibold", 20), text=combobox_apps.get(),
                           fg='#FFFFFF')
    app_name_label.place(x=40, y=50)

    # ==================== Update App Username =====================
    update_username_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                                  fg='#FFFFFF',
                                  bd=0)
    update_username_entry.place(x=40, y=170, width=266, height=50)
    update_username_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    update_username_label = Label(win, text='• New Username', fg="#FFFFFF", bg='#272A37',
                                  font=("yu gothic ui", 11, 'bold'))
    update_username_label.place(x=40, y=140)
    # ===================== Update App Password =====================
    update_pass_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1, fg='#FFFFFF',
                              bd=0)
    update_pass_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    update_pass_entry.place(x=40, y=260, width=266, height=50)
    update_pass_label = Label(win, text='• New Password', fg="#FFFFFF", bg='#272A37',
                              font=("yu gothic ui", 11, 'bold'))
    update_pass_label.place(x=40, y=230)
    # ====================== Update App Email =======================
    update_email_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                               fg='#FFFFFF',
                               bd=0)
    update_email_entry.place(x=40, y=350, width=266, height=50)
    update_email_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    update_email_label = Label(win, text='• Email', fg="#FFFFFF", bg='#272A37',
                               font=("yu gothic ui", 11, 'bold'))
    update_email_label.place(x=40, y=320)
    # ====================== Random and Submit buttons ====================
    change_btn = Button(win, fg='#f8f8f8', text='Submit Changes', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                        cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                        command=lambda: update_details(combobox_apps.get(), update_username_entry.get(),
                                                       update_pass_entry.get(), update_email_entry.get())
                        )
    change_btn.place(x=40, y=410, width=128, height=45)
    random_btn = Button(win, fg='#f8f8f8', text='Random', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                        cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                        command=lambda: random_btn_fnc()
                        )
    random_btn.place(y=260, x=240, height=50)

    def random_btn_fnc():
        """Insert into update_pass_entry a string characters"""
        update_pass_entry.delete(0, END)
        update_pass_entry.insert(0, random_pass_generator())

    def update_details(app_name, update_username, update_password, update_email):
        """
        Updates application login info into database, uses PasswordApp module to update the table
        """
        pm.AppLoginInfo.update_details(user_id, app_name, update_username, update_password, update_email)
        exit_window(win)


def exit_window(win):
    win.destroy()


# Windows Size and Placement

password_manager = Tk()
password_manager.rowconfigure(0, weight=1)
password_manager.columnconfigure(0, weight=1)
height = 540
width = 960
x = (password_manager.winfo_screenwidth() // 2) - (width // 2)
y = (password_manager.winfo_screenheight() // 4) - (height // 4)
password_manager.geometry('{}x{}+{}+{}'.format(width, height, x, y))
password_manager.title('Password Manager')

# Navigating through windows/frames
login = Frame(password_manager)
sign_up = Frame(password_manager)
frame_app = Frame(password_manager)
# get_pass_frame = Frame(password_manager)
# add_app_frame = Frame(password_manager)

for frame in (login, sign_up, frame_app,):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(the_frame):
    """Raises the desired frame"""
    the_frame.tkraise()


show_frame(login)
user_id = ''  # Global variable

# ================================================
# +++++++++++SIGN UP PAGE STARTS HERE+++++++++++++
# ================================================

# Sign Up Text Variables
username = StringVar()
email = StringVar()
password = StringVar()
confirm_password = StringVar()

# ================Background Image ====================
sign_up.configure(bg="#525561")
backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_image = Label(sign_up, image=backgroundImage, bg="#525561")
bg_image.pack()
# ================ Header Text Left ====================
headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
headerText_image_label1 = Label(bg_image, image=headerText_image_left, bg="#272A37")
headerText_image_label1.place(x=60, y=45)
headerText1 = Label(bg_image, text="Password Manager", fg="#FFFFFF", font=("yu gothic ui bold", 30 * -1), bg="#272A37")
headerText1.place(x=110, y=45)
# ================ CREATE ACCOUNT HEADER ====================
createAccount_header = Label(bg_image, text="Create new account", fg="#FFFFFF", font=("yu gothic ui Bold", 28 * -1),
                             bg="#272A37")
createAccount_header.place(x=75, y=121)
# ================ ALREADY HAVE AN ACCOUNT TEXT ====================
text = Label(bg_image, text="Already a member?", fg="#FFFFFF", font=("yu gothic ui Regular", 15 * -1), bg="#272A37")
text.place(x=75, y=187)
# ================ GO TO LOGIN ====================
switchLogin = Button(bg_image, text="Login", fg="#206DB4", font=("yu gothic ui Bold", 15 * -1), bg="#272A37", bd=0,
                     cursor="hand2", activebackground="#272A37", activeforeground="#ffffff",
                     command=lambda: show_frame(login))
switchLogin.place(x=230, y=185, width=50, height=35)
# ================ Username Section ====================
username_image = PhotoImage(file="assets/email_username.png")
username_image_Label = Label(bg_image, image=username_image, bg="#272A37")
username_image_Label.place(x=80, y=242)

username_text = Label(username_image_Label, text="Username", fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1),
                      bg="#3D404B")
username_text.place(x=25, y=0)

username_icon = PhotoImage(file="assets/username_icon.png")
username_icon_Label = Label(username_image_Label, image=username_icon, bg="#3D404B")
username_icon_Label.place(x=370, y=15)

username_entry = Entry(username_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                       font=("yu gothic ui SemiBold", 16 * -1), textvariable=username)
username_entry.place(x=8, y=17, width=354, height=27)
# ================ Email Name Section ====================
emailName_image = PhotoImage(file="assets/email_username.png")
emailName_image_Label = Label(bg_image, image=emailName_image, bg="#272A37")
emailName_image_Label.place(x=80, y=311)

emailName_text = Label(emailName_image_Label, text="Email account", fg="#FFFFFF",
                       font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
emailName_text.place(x=25, y=0)

emailName_icon = PhotoImage(file="assets\\email-icon.png")
emailName_icon_Label = Label(emailName_image_Label, image=emailName_icon, bg="#3D404B")
emailName_icon_Label.place(x=370, y=15)

emailName_entry = Entry(emailName_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                        font=("yu gothic ui SemiBold", 16 * -1), textvariable=email)
emailName_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
passwordName_image = PhotoImage(file="assets\\input_img.png")
passwordName_image_Label = Label(bg_image, image=passwordName_image, bg="#272A37")
passwordName_image_Label.place(x=80, y=380)

passwordName_text = Label(passwordName_image_Label, text="Password", fg="#FFFFFF",
                          font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
passwordName_text.place(x=25, y=0)

passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
passwordName_icon_Label = Label(passwordName_image_Label, image=passwordName_icon, bg="#3D404B")
passwordName_icon_Label.place(x=159, y=15)

passwordName_entry = Entry(passwordName_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                           font=("yu gothic ui SemiBold", 16 * -1), textvariable=password, show="*",)
passwordName_entry.place(x=8, y=17, width=140, height=27)

# ================ Confirm Password Name Section ====================
confirm_passwordName_image = PhotoImage(file="assets\\input_img.png")
confirm_passwordName_image_Label = Label(bg_image, image=confirm_passwordName_image, bg="#272A37")
confirm_passwordName_image_Label.place(x=293, y=380)

confirm_passwordName_text = Label(confirm_passwordName_image_Label, text="Confirm Password", fg="#FFFFFF",
                                  font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
confirm_passwordName_text.place(x=25, y=0)

confirm_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
confirm_passwordName_icon_Label = Label(confirm_passwordName_image_Label, image=confirm_passwordName_icon, bg="#3D404B")
confirm_passwordName_icon_Label.place(x=159, y=15)

confirm_passwordName_entry = Entry(confirm_passwordName_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                                   font=("yu gothic ui SemiBold", 16 * -1), textvariable=confirm_password, show="*")
confirm_passwordName_entry.place(x=8, y=17, width=140, height=27)

# =============== Submit Button ====================
submit_buttonImage = PhotoImage(file="assets\\button_1.png")
submit_button = Button(bg_image, image=submit_buttonImage, borderwidth=0, highlightthickness=0, relief="flat",
                       activebackground="#272A37", cursor="hand2", command=lambda: signup(),)
submit_button.place(x=130, y=460, width=333, height=65)

# ================ Header Text Down ====================
headerText3 = Label(bg_image, text="Powered by Marcu Gabriel", fg="#FFFFFF", font=("yu gothic ui bold", 20 * -1), bg="#272A37")
headerText3.place(x=680, y=480)

# ===================================================================
# +++++++++++++++++++++ LOGIN PAGE STARTS HERE+++++++++++++++++++++++
# ===================================================================
# Login text variables
login_username = StringVar()
login_password = StringVar()

login.configure(bg="#525561")

# ================Background Image ====================
login_bg_image = PhotoImage(file="assets\\image_1.png")
bg_image_login = Label(login, image=login_bg_image, bg="#525561")
bg_image_login.pack()

# ================ Header Text Left ====================
login_header_text_image_left = PhotoImage(file="assets\\headerText_image.png")
login_header_text_image_label1 = Label(bg_image_login, image=login_header_text_image_left, bg="#272A37")
login_header_text_image_label1.place(x=60, y=45)

login_header_text1 = Label(bg_image_login, text="Password Manager", fg="#FFFFFF", font=("yu gothic ui bold", 30 * -1),
                           bg="#272A37")
login_header_text1.place(x=110, y=45)

# ================ LOGIN TO ACCOUNT HEADER ====================
login_account_header = Label(bg_image_login, text="Login to continue", fg="#FFFFFF",
                             font=("yu gothic ui Bold", 28 * -1), bg="#272A37")
login_account_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
login_text = Label(bg_image_login, text="Not a member?", fg="#FFFFFF", font=("yu gothic ui Regular", 15 * -1),
                   bg="#272A37")
login_text.place(x=75, y=187)

# ================ GO TO SIGN UP ====================
switch_signup = Button(bg_image_login, text="Sign Up", fg="#206DB4", font=("yu gothic ui Bold", 15 * -1), bg="#272A37",
                       bd=0, cursor="hand2", activebackground="#272A37", activeforeground="#ffffff",
                       command=lambda: show_frame(sign_up))
switch_signup.place(x=220, y=185, width=70, height=35)

# ================ Email Name Section ====================
login_username_image = PhotoImage(file="assets/email_username.png")
login_username_image_label = Label(bg_image_login, image=login_username_image, bg="#272A37")
login_username_image_label.place(x=76, y=242)

login_username_text = Label(login_username_image_label, text="Username", fg="#FFFFFF",
                            font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
login_username_text.place(x=25, y=0)

login_username_icon = PhotoImage(file="assets\\username_icon.png")
login_username_icon_label = Label(login_username_image_label, image=login_username_icon, bg="#3D404B")
login_username_icon_label.place(x=370, y=15)

login_username_entry = Entry(login_username_image_label, bd=0, bg="#3D404B", highlightthickness=0,
                             font=("yu gothic ui SemiBold", 16 * -1), textvariable=login_username,)
login_username_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
login_password_name_image = PhotoImage(file="assets/email_username.png")
login_password_name_image_label = Label(bg_image_login, image=login_password_name_image, bg="#272A37")
login_password_name_image_label.place(x=80, y=330)

login_password_name_text = Label(login_password_name_image_label, text="Password", fg="#FFFFFF",
                                 font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
login_password_name_text.place(x=25, y=0)

login_password_name_icon = PhotoImage(file="assets\\pass-icon.png")
login_password_name_icon_label = Label(login_password_name_image_label, image=login_password_name_icon, bg="#3D404B")
login_password_name_icon_label.place(x=370, y=15)

login_password_name_entry = Entry(login_password_name_image_label, bd=0, show='*', bg="#3D404B", highlightthickness=0,
                                  font=("yu gothic ui SemiBold", 16 * -1), textvariable=login_password)
login_password_name_entry.place(x=8, y=17, width=354, height=27)

# =============== Submit Button ====================
login_button_image_1 = PhotoImage(file="assets\\button_1.png")
login_button_1 = Button(bg_image_login, image=login_button_image_1, borderwidth=0, highlightthickness=0, relief="flat",
                        activebackground="#272A37", cursor="hand2", command=lambda: login_user())
login_button_1.place(x=120, y=445, width=333, height=65)

# ================ Header Text Down ====================
login_header_text3 = Label(bg_image_login, text="Powered by Marcu Gabriel", fg="#FFFFFF",
                           font=("yu gothic ui bold", 20 * -1), bg="#272A37")
login_header_text3.place(x=680, y=480)

# ================ Forgot Password ====================
forgot_password_btn = Button(bg_image_login, text="Forgot Password", fg="#206DB4", font=("yu gothic ui Bold", 15 * -1),
                             bg="#272A37", bd=0, activebackground="#272A37", activeforeground="#ffffff", cursor="hand2",
                             command=lambda: forgot_password(),)
forgot_password_btn.place(x=210, y=400, width=150, height=35)

# ================================================
# ++++++++++ Application starts here +++++++++++++
# ================================================
frame_app.configure(bg='#272A37')
bg_img: PhotoImage = PhotoImage(file="assets\\image_1.png")
bg_label = Label(frame_app, image=bg_img)

# ==============GET PASS FRAME=====================
select_app_label = Label(bg_label, text="GET PASSWORD", font=('Constntia', 20), bg='#272A37', fg="white")
select_app_label.place(y=15, x=75)

apps_l = app_list()
combobox_apps = ttk.Combobox(bg_label, width=24, font=('Helvetica', 20), values=apps_l, )
combobox_apps.set("Pick an app")
combobox_apps.place(y=70, x=50)

get_button = Button(bg_label, fg='#f8f8f8', text='Get', bg='#1D90F5', font=("yu gothic ui", 14, "bold"), width=9,
                    cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                    command=app_details)
get_button.place(y=120, x=50)
update_button = Button(bg_label, fg='#f8f8f8', text='Update', bg='#1D90F5', font=("yu gothic ui", 14, "bold"), width=9,
                       cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                       command=update_details_window)
update_button.place(y=120, x=190)

remove_button = Button(bg_label, fg='#f8f8f8', text='Remove', bg='#B45D25', font=("yu gothic ui", 14, "bold"), width=9,
                       cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                       command=lambda: remove_app())
remove_button.place(y=120, x=330)
listbox_details = Listbox(bg_label, bg="#272A37", fg='white', width=25, font=('Constntia', 20))
listbox_details.place(y=170, x=50)

# =================== Add new app Link=================
bg_img_app2 = PhotoImage(file='assets/add_app.png')
add_password_btn = Button(bg_label, image=bg_img_app2, bg="#272A37", font=("yu gothic ui Bold", 28 * -1),
                          cursor='hand2', command=add_new_app_frame)
add_password_btn.place(y=198, x=527)
add_password_label = Label(bg_label, text="ADD NEW APP", bg='#272A37', font=("yu gothic ui Bold", 20 * -1),
                           width=21, height=1, fg='white',)
add_password_label.place(y=160, x=527)
# ================= Log out ==================
logout_btn = Button(bg_label, fg='#f8f8f8', text='LOG OUT', bg='#1D90F5', font=("yu gothic ui", 14, "bold"), width=8,
                    cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5",
                    command=lambda: logout())
logout_btn.place(y=15, x=850)
bg_label.pack()

app_header_text = Label(bg_label, text="Powered by Marcu Gabriel", fg="#FFFFFF", font=("yu gothic ui bold", 20 * -1),
                        bg="#272A37")
app_header_text.place(x=680, y=480)


password_manager.resizable(False, False)
password_manager.mainloop()

if __name__ == "__main__":
    print(user_id)
