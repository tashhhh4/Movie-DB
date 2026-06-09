import db

class UserManager: # Singleton

    _active_user = None

    @classmethod
    def login(cls, user_name):
        # Check that the user is real from the DB
        # error if user not found
        cls._active_user = user_name

    @classmethod
    def logout(cls):
        cls._active_user = None
    
    @classmethod
    def get_user(cls):
        return cls._active_user
    
    @classmethod
    def create_user(cls, user_name):
        users = db.get_all_users()
        if user_name in users:
            print(f"A user with the name\"{user_name}\" already exists. Please choose a different name.")
            return
        db.add_user(user_name)
        print(f"User {user_name} was created.")

    @classmethod
    def get_all_users(cls):
        return db.get_all_users()