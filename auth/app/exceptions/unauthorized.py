class UnauthorizedException(Exception):
    def __init__(self, credential_id):
        self.message = f"User {credential_id} is not authorized to perform this operation."
        self.code = 401

    def __str__(self):
        return self.message
