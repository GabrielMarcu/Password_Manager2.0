"""
Create objects of type PasswordApp and saves them into database or remove them from there
"""
import sqlite3
from tkinter import messagebox


# import login_register as log


class PasswordApp():


    def __init__(self, app_name, username, password, email):

        self.app_name = app_name
        self.username = username
        self.password = password
        self.email = email

    def register_app(self):

        try:
            with open("log.txt", 'r') as fr:
                read = ''.join(fr.readlines())
            # print(read)
                connection = sqlite3.connect("./Database/password_manager.db")
                query = "INSERT INTO app_table(user_id, app_name, username, password, email) VALUES(?,?,?,?,?)"
                # find_id = f"SELECT * FROM login_table WHERE username={read}"
                cursor = connection.cursor()
                # cursor.execute("SELECT count(*) FROM app_table;")
                id_query = cursor.execute(f"SELECT id FROM login_table WHERE username=?")
                user_id = cursor.execute(id_query, read)
                print(user_id)
                cursor.execute(query, (user_id, self.app_name, self.username, self.password, self.email))
                connection.commit()
                connection.close()
                messagebox.showinfo("Congrats!", "App successfully added in database")

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Attention!", "App already registered in database")

    @staticmethod
    def remove_app(existing_app_name):
        connection = sqlite3.connect("./Database/password_manager.db")
        querry = f"DELETE FROM app_table WHERE app_name='{existing_app_name}'"
        cursor = connection.cursor()
        cursor.execute(querry)
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Application login info removed from database")

    @staticmethod
    def empty_db():
        connection = sqlite3.connect("./Database/password_manager.db")
        querry = "DELETE FROM app_table"
        cursor = connection.cursor()
        cursor.execute(querry)
        connection.commit()
        connection.close()

    @staticmethod
    def get_app_list():
        try:
            connection = sqlite3.connect("Database/password_manager.db")
            cur = connection.cursor()
            find_app = "SELECT  app_name FROM app_table"
            cur.execute(find_app)
            result = cur.fetchall()
            print(list(result))
            return result
        except Exception as e:
            print(f'{e}, error in get_app_list')

    @staticmethod
    def random_pass():
        pass


if __name__ == "__main__":
    # new_app = PasswordApp('youtube', 'gabi', '12345', 'gabi@gmail.com')
    # new_app.register_app()
    # PasswordApp.remove_app('git')
    # PasswordApp.empty_db()
    # #
    # new_app2 = PasswordApp('google', 'gabi_google', 'g00613', 'gabi@gmail.com')
    # new_app2.register_app()
    # new_app3 = PasswordApp('git', 'gabi', "1111", 'g@gmail.com')
    # new_app3.register_app()
    # new_app4 = PasswordApp('aaa', 'gabi', "1111", 'ga@gmail.com')
    # new_app4.register_app()
    # print(PasswordApp.id)
    PasswordApp.get_app_list()
