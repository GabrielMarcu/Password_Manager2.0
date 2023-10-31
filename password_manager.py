"""
Class PasswordApp with its methods:
### register_app #Saves PasswordApp object into database

### remove_app ->Removes PasswordApp object from database

### empty_app_table ->Deletes all PasswordApp objects from app_table in database

### get_app_list ->Returns a list of app names from database for a specific user_id

### update_details ->Modifies username, password and email for a specific app_name and user_id in database
"""

import sqlite3
from tkinter import messagebox


class PasswordApp:
    """
    Creates, updates objects in database or removes objects from database
    """
    def __init__(self, app_name, username, password, email):
        self.app_name = app_name
        self.username = username
        self.password = password
        self.email = email

    def register_app(self, user_id: str) -> None:
        """
        Saves PasswordApp object into database
        """
        try:
            connection = sqlite3.connect("./Database/password_manager.db")
            query = "INSERT INTO app_table(user_id, app_name, username, password, email) VALUES(?,?,?,?,?)"
            cursor = connection.cursor()
            cursor.execute(query, (user_id, self.app_name, self.username, self.password, self.email))
            connection.commit()
            connection.close()
            messagebox.showinfo("Congrats!", "App successfully added in database")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Attention!", "App already registered in database")

    @staticmethod
    def remove_app(existing_app_name: str, user_id: str) -> None:
        """
        Removes PasswordApp object from database
        """
        connection = sqlite3.connect("./Database/password_manager.db")
        query = "DELETE FROM app_table WHERE app_name=? and user_id=?"
        cursor = connection.cursor()
        cursor.execute(query, (existing_app_name, user_id))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Application login info removed from database")

    @staticmethod
    def empty_app_table_db():
        """
        Deletes all PasswordApp objects from app_table in database
        """
        connection = sqlite3.connect("./Database/password_manager.db")
        querry = "DELETE FROM app_table"
        cursor = connection.cursor()
        cursor.execute(querry)
        connection.commit()
        connection.close()

    @staticmethod
    def get_app_list(user_id: str) -> list:
        """
        Returns a list of app names from database for a specific user_id
        """
        try:
            connection = sqlite3.connect("Database/password_manager.db")
            cur = connection.cursor()
            find_app = "SELECT app_name FROM app_table WHERE user_id=?"
            cur.execute(find_app, user_id)
            result = cur.fetchall()
            print(list(result))
            return result
        except IndexError as e:
            result = []
            return result

            # print(f'{e}, error in get_app_list')

    @staticmethod
    def update_details(user_id: str, app_name: str, username: str, password: str, email: str) -> None:
        """
        Modifies username, password and email for a specific app_name and user_id in database
        """
        connection = sqlite3.connect('Database/password_manager.db')
        query = """UPDATE app_table SET username = ?,  password = ?, email = ?
                    WHERE app_name = ? and user_id=?"""
        cursor = connection.cursor()
        cursor.execute(query, (username, password, email, app_name, user_id))
        connection.commit()
        connection.close()



if __name__ == "__main__":
    # new_app = PasswordApp('youtube', 'gabi', '12345', 'gabi@gmail.com')
    # new_app.register_app()
    # PasswordApp.remove_app('instagram', '6')
    # PasswordApp.empty_db()
    # new_app2 = PasswordApp('google', 'gabi_google', 'g00613', 'gabi@gmail.com')
    # new_app2.register_app()
    # new_app3 = PasswordApp('git', 'gabi', "1111", 'g@gmail.com')
    # new_app3.register_app()
    # new_app4 = PasswordApp('aaa', 'gabi', "1111", 'ga@gmail.com')
    # new_app4.register_app()
    # print(PasswordApp.id)
    # PasswordApp.get_app_list()
    pass