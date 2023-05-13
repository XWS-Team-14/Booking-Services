class EmailAlreadyTakenException(Exception):
    def __init__(self, email):
        self.message = f"The email {email} has already been taken."
        self.code = 409

    def __str__(self):
        return self.message
