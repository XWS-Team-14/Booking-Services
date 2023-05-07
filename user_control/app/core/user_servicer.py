from proto import user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServiceServicer):
    async def Register(self, request, context):
        """ Registers user.
            Input: ID, first name, last name, home address, gender.
            Output: Empty, or error. """

    async def GetById(self, request, context):
        """ Gets user by their ID.
            Input: ID.
            Output: User information (ID, first name, last name, home address, gender), or error. """

    async def Update(self, request, context):
        """ Updates user's information.
            Input: ID, first name, last name, home address, gender.
            Output: Empty, or error. """

    async def Delete(self, request, context):
        """ Deletes user's information.
            Input: ID.
            Output: Empty, or error. """
