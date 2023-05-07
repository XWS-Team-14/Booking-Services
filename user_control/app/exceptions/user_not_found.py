class UserNotFoundException(Exception):
    def __init__(self, user_id=None):
        self.code = 404
        if user_id:
            self.message = f"User with the id {user_id} was not found."
        else:
            self.message = "User with the given id was not found."

    def __str__(self):
        return self.message
