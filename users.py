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
        # Use DB to create a new user
        # Error if a user with the same name already exists
        print(f"We want to add '{user_name}' (Not yet implemented).")

    @classmethod
    def get_all_users(cls):
        # Use DB to lookup users
        # convert to simple list of strings

        #temp
        users = ["Natasha", "Dan", "Laura"]

        return users