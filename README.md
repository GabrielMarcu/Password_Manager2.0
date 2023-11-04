# Password_Manager2.0
Application made for safely saving login info(passwords, usernames etc.) for any web apps you desire. You can add, update or delete login info in database, it can store data safely for more than one user
## Modules:
### password_manager
"""
Class PasswordApp with its methods:

*** register_app #Saves PasswordApp object into database

*** remove_app ->Removes PasswordApp object from database

*** empty_app_table ->Deletes all PasswordApp objects from app_table in database

*** get_app_list ->Returns a list of app names from database for a specific user_id

*** update_details ->Modifies username, password and email for a specific app_name and user_id in database
"""
### login_register
"""
First of all runs Database/create_database.py

Tkinter GUI used for saving account details for any aplication the user wants.

FRAMES: login, sign_up, frame_app

global variables: user_id,  apps_l(a list of apps for a specific user_id)

Functions:

-->signup -> Used for SUBMIT button in Sign up frame. Adds new user information in database

-->login_user ->  Checks is user exists in database, and logs in the app frame

-->forgot_password -> Opens a new window used for resetting login password

-->change_password -> Resets login password, based on email from database

-->get_app list -> Returns a list of all apps registered in database for a specific user_id

-->app_details -> Returns a list of login details of the selected app

-->update_details_window -> Opens a new window used for updating login info about and app
"""

### GUI Video
[![Watch the video](https://img.youtube.com/vi/OKB0HTz2Y4g/hqdefault.jpg)](https://www.youtube.com/watch?v=OKB0HTz2Y4g)

