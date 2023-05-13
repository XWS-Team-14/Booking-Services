class UnauthorizedException(Exception):
    def __init__(self, credential_id=None, email=None):
        if credential_id:
            self.message = f"User {credential_id} is not authorized to perform this operation."
        elif email:
            self.message = f"User {email} is not authorized to perform this operation."
        else:
            self.message = "Unauthorized: missing or invalid credentials."
        self.code = 401

    def __str__(self):
        return self.message
