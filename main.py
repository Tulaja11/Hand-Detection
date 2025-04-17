from database import Database
from login_ui import ModernLoginUI
from dashboard import Dashboard
from quiz_app import MCQApp

def main():
    try:

        db = Database()
        

        login_window = ModernLoginUI(db)
        user_id = login_window.run()
        

        if user_id:
            print(f"Successfully logged in with user_id: {user_id}")  # Debug print
            dashboard = Dashboard(user_id, db)
            dashboard.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
