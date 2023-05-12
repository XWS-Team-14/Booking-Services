class UserNotFoundException(Exception):
    def __init__(self, email=None, credential_id=None):
        self.code = 404
        if email:
            self.message = f"User with the email {email} was not found."
        elif credential_id:
            self.message = f"User with the id {credential_id} was not found."
        else:
            self.message = "User with the given credentials was not found."

    def __str__(self):
        return self.message
