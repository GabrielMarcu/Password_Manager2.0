import sqlite3


def login_db():
    connection = sqlite3.connect('password_manager.db')
    create_login = """
        CREATE TABLE IF NOT EXISTS login_table (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        username TEXT(32) NOT NULL,
        password TEXT(32) NOT NULL,
        email TEXT(32)
        
        );"""

    cur = connection.cursor()

    cur.execute(create_login)
    connection.commit()
    connection.close()


def app_db():

    connection = sqlite3.connect('password_manager.db')
    create_command = """
            CREATE TABLE IF NOT EXISTS app_table (
            user_id INTEGER NOT NULL,
            app_name TEXT(16) NOT NULL,
            username TEXT(32) NOT NULL,
            password TEXT(32) NOT NULL,
            email TEXT(32),
            FOREIGN KEY (user_id) REFERENCES login_table(id)
        ); """

    cur = connection.cursor()

    cur.execute(create_command)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    login_db()
    app_db()