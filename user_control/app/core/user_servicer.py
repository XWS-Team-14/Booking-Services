import uuid

from app.exceptions.user_not_found import UserNotFoundException
from app.models.gender import Gender
from app.models.user import User
from proto import user_pb2_grpc, user_pb2


class UserServicer(user_pb2_grpc.UserServiceServicer):
    async def Register(self, request, context):
        """ Registers user.
            Input: ID, first name, last name, home address, gender.
            Output: Empty, or error. """
        user = User(
            id=uuid.UUID(request.id),
            first_name=request.first_name,
            last_name=request.last_name,
            home_address=request.home_address,
            gender=Gender(request.gender)
        )
        await user.insert()
        return user_pb2.EmptyMessage()

    async def GetById(self, request, context):
        """ Gets user by their ID.
            Input: ID.
            Output: User information (ID, first name, last name, home address, gender), or error. """
        try:
            user = await User.find_one(User.id == request.id)
            if user is None:
                raise UserNotFoundException(user_id=request.id)
            return user_pb2.UserResponse(id=user.id, first_name=user.first_name, last_name=user.last_name, home_address=user.home_address, gender=user.gender.value)
        except UserNotFoundException as error:
            return user_pb2.UserResponse(id=user.id, error_message=error.message,
                                                     error_code=error.code)

    async def Update(self, request, context):
        """ Updates user's information.
            Input: ID, first name, last name, home address, gender.
            Output: Empty, or error. """
        try:
            user = await User.find_one(User.id == request.id)
            if user is None:
                raise UserNotFoundException(user_id=request.id)
            new_user = User(
                id=request.id,
                first_name=request.first_name,
                last_name=request.last_name,
                home_address=request.home_address,
                gender=Gender(request.gender))
            await new_user.replace()
            return user_pb2.EmptyMessage()
        except UserNotFoundException as error:
            return user_pb2.EmptyMessage(error_message=error.message, error_code=error.code)

    async def Delete(self, request, context):
        """ Deletes user's information.
            Input: ID.
            Output: Empty, or error. """
        try:
            user = await User.find_one(User.id == request.id)
            if user is None:
                raise UserNotFoundException(user_id=request.id)
            await user.delete()
            return user_pb2.EmptyMessage()
        except UserNotFoundException as error:
            return user_pb2.EmptyMessage(error_message=error.message, error_code=error.code)
