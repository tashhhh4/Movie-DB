import movie_storage.movie_storage_sql as db

class UserManager: # Singleton

    _active_user = None

    @classmethod
    def login(cls, user_id):
        user = db.get_user(user_id)
        cls._active_user = user

    @classmethod
    def logout(cls):
        cls._active_user = None
    
    @classmethod
    def get_current_user(cls):
        return cls._active_user
    
    @classmethod
    def create_user(cls, user_name):
        users = db.list_users()
        if user_name in users:
            print(f"A user with the name\"{user_name}\" already exists. Please choose a different name.")
            return
        db.add_user(user_name)
        print(f"User {user_name} was created.")

    @classmethod
    def get_all_users(cls):
        return db.list_users()
    
    @classmethod
    def get_user(cls, user_id):
        return db.get_user(user_id)