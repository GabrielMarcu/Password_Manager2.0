"""
This is a GUI form for Login and Register user

"""

from tkinter import *
from tkinter import messagebox, PhotoImage, ttk
import GUI
import sqlite3
import password_manager as pm


# from PIL import Image, ImageTk

# ===============================
# DATABASE CONNECTION FOR SIGN UP
# ===============================


def signup():
    if GUI.username_entry.get() == "" or GUI.emailName_entry.get() == "" or GUI.passwordName_entry.get() == "" or \
            GUI.confirm_passwordName_entry.get() == "":
        messagebox.showerror("Error", "All Fields Are Required")

    elif GUI.passwordName_entry.get() != GUI.confirm_passwordName_entry.get():
        messagebox.showerror('Error', "Password and Confirm Password Didn't Match")

    else:
        try:

            connection = sqlite3.connect("Database/password_manager.db")
            cur = connection.cursor()
            cur.execute("SELECT count(*) FROM login_table;")
            id = cur.fetchall()[0][0] + 1
            cur.execute("INSERT INTO login_table(id, username, password, email) VALUES(?,?,?,?)",
                        (id, GUI.username_entry.get(), GUI.passwordName_entry.get(), GUI.emailName_entry.get()))
            connection.commit()
            connection.close()
            clear_sign_up()
            messagebox.showinfo("Success", "New Account Created")
            GUI.show_frame(GUI.login)
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong, please try again")
            print(e)


# Clear sign up fields


def clear_sign_up():
    GUI.username.set("")
    GUI.email.set("")
    GUI.password.set("")
    GUI.confirm_password.set("")


# ======== DATABASE CONNECTION FOR LOGIN ==========


def login_user():
    try:
        connection = sqlite3.connect("Database/password_manager.db")
        cur = connection.cursor()
        find_user = "SELECT * FROM login_table WHERE username = ? and password = ?;"
        cur.execute(find_user, [(GUI.login_username_entry.get()), (GUI.login_password_name_entry.get())])

        result = cur.fetchall()

        if result:
            with open('log.txt', 'w') as fw:
                fw.write(GUI.login_username_entry.get())
            clear_login()
            messagebox.showinfo("Success", "Logged in Successfully")
            GUI.show_frame(GUI.frame_app)
        elif GUI.login_username_entry.get() == "" or GUI.login_password_name_entry.get() == "":
            messagebox.showerror("Warning", 'All fields are required')
        else:
            messagebox.showerror("Failed", "Incorrect username or password, pleas try again or sign up")

    except Exception as e:
        messagebox.showerror("Error", "Something went wrong, please try again")
        print(f'{e} happens after login_user')


# ======= Clear login fields ============


def clear_login():
    GUI.login_username.set("")
    GUI.login_password.set("")


def exit_window():
    GUI.win.destroy()

 # DATABASE CONNECTION FOR FORGOT PASSWORD


def change_password():
    try:
        if GUI.email_entry3.get == "" or GUI.new_password_entry.get() == "":
            messagebox.showerror("Error", "All Fields Are Required")
            exit_window()

        else:
            db = sqlite3.connect("./Database/password_manager.db")
            cursor = db.cursor()
            querry = "SELECT * FROM login_table WHERE email=?"
            cursor.execute(querry, [(GUI.email_entry3.get())])
            row = cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Email does not exist")
                exit_window()
            else:
                querry = "UPDATE login_table SET password=? where Email=?"
                cursor.execute(querry, [GUI.new_password_entry.get(), GUI.email_entry3.get(), ])
                db.commit()
                db.close()
                messagebox.showinfo("Well Done", "Password Successfully Changed")
                exit_window()
    except Exception as e:
        print("Error", f'{e}, happened in change_password function')




if __name__ == "__main__":
    pass
