import uuid

from jwt import InvalidTokenError, ExpiredSignatureError
from loguru import logger
from passlib.hash import bcrypt
from proto import credential_pb2, credential_pb2_grpc
from ..exceptions.email_already_taken import EmailAlreadyTakenException
from ..exceptions.unauthorized import UnauthorizedException
from ..exceptions.user_not_found import UserNotFoundException
from ..models.credential import Credential
import jwt
from datetime import datetime, timedelta
from ..constants import JWT_ACCESS_SECRET, JWT_REFRESH_SECRET

from ..models.role import Role


class CredentialServicer(credential_pb2_grpc.CredentialServiceServicer):

    async def Register(self, request, context):
        """ Registers credentials.
            Input: ID, email, password, role.
            Output: Empty, or error. """
        try:
            logger.info('Request received')
            existing_credential = await Credential.find_one(Credential.email == request.email)
            if existing_credential is not None:
                raise EmailAlreadyTakenException(email=request.email)
            credential = Credential(
                id=uuid.UUID(request.id),
                email=request.email,
                password=bcrypt.hash(request.password),
                role=Role(request.role))
            await credential.insert()
            logger.success("User {} successfully registered.", request.email)
            return credential_pb2.Empty()
        except EmailAlreadyTakenException as error:
            return credential_pb2.Empty(error_message=error.message, error_code=error.code)

    async def Login(self, request, context):
        """ Logs in user.
            Input: Email, password.
            Output: JWT access token, JWT refresh token, or error. """
        try:
            logger.info('Request received')
            credential = await Credential.find_one(Credential.email == request.email)
            if credential is None or not bcrypt.verify(request.password, credential.password):
                logger.error("Unsuccessful login: {}", request.email)
                raise UnauthorizedException()
            access_token = jwt.encode({
                "id": str(credential.id),
                "role": credential.role.value,
                "exp": datetime.utcnow() + timedelta(minutes=30)
            }, JWT_ACCESS_SECRET)
            refresh_token = jwt.encode({
                "id": str(credential.id),
                "role": credential.role.value,
                "exp": datetime.utcnow() + timedelta(days=7)
            }, JWT_REFRESH_SECRET)
            logger.success("User {} logged in.", request.email)
            return credential_pb2.Token(access_token=access_token, refresh_token=refresh_token)
        except UnauthorizedException as error:
            return credential_pb2.Token(access_token="", error_message=error.message, error_code=error.code)

    async def GetById(self, request, context):
        """ Gets credentials by ID.
            Input: ID.
            Output: Credentials, or error. """
        try:
            credential = await Credential.find_one(Credential.id == uuid.UUID(request.id))
            if credential is None:
                raise UserNotFoundException(credential_id=request.id)
            return credential_pb2.CredentialResponse(id=credential.id, email=credential.email, role=credential.role,
                                                     active=credential.active)
        except UserNotFoundException as error:
            return credential_pb2.CredentialResponse(id="", email="", error_message=error.message,
                                                     error_code=error.code)

    async def GetByEmail(self, request, context):
        """ Gets credentials by email.
            Input: Email.
            Output: Credentials, or error. """
        try:
            credential = await Credential.find_one(Credential.email == request.email)
            if credential is None:
                raise UserNotFoundException(email=request.email)
            return credential_pb2.CredentialResponse(id=credential.id, email=credential.email, role=credential.role,
                                                     active=credential.active)
        except UserNotFoundException as error:
            return credential_pb2.CredentialResponse(id="", email=request.email, error_message=error.message,
                                                     error_code=error.code)

    async def GetActive(self, request, context):
        """ Validates access token and gets active user's credentials.
            Input: JWT access token.
            Output: ID, email, or error. """
        try:
            payload = jwt.decode(request.access_token, JWT_ACCESS_SECRET)
            credential = await Credential.find_one(Credential.id == payload.get("id"))
            if credential is None:
                raise UserNotFoundException(credential_id=payload.get("id"))
            return credential_pb2.ActiveResponse(id=credential.id, email=credential.email)
        except InvalidTokenError:
            return credential_pb2.ActiveResponse(id="", email="", error_message="Invalid access token.", error_code=498)
        except UserNotFoundException as error:
            return credential_pb2.ActiveResponse(id="", email="", error_message=error.message, error_code=error.code)

    async def UpdateEmail(self, request, context):
        """ Updates email.
            Input: ID, old email, new email.
            Output: Empty, or error. """
        try:
            credential = await Credential.find_one(Credential.id == uuid.UUID(request.id))
            if credential is None or credential.email != request.old_email:
                raise UserNotFoundException(email=request.old_email)
            await credential.set({Credential.email: request.new_email})
            logger.success("Email updated.")
            return credential_pb2.Token()
        except UserNotFoundException as error:
            return credential_pb2.Empty(error_message=error.message, error_code=error.code)

    async def UpdatePassword(self, request, context):
        """ Updates password.
            Input: ID, old password, new password.
            Output: Empty, or error. """
        try:
            credential = await Credential.find_one(Credential.id == uuid.UUID(request.id))
            if credential is None or not bcrypt.verify(request.old_password, credential.password):
                logger.error(f"Unsuccessful password change for user {request.id}.")
                raise UserNotFoundException()
            await credential.set({Credential.password: bcrypt.hash(request.new_password)})
            logger.success("Password updated.")
            return credential_pb2.Empty()
        except UserNotFoundException as error:
            return credential_pb2.Empty(error_message=error.message, error_code=error.code)

    async def Delete(self, request, context):
        """ Deletes credentials.
            Input: ID.
            Output: Empty, or error. """
        try:
            credential = await Credential.find_one(Credential.id == uuid.UUID(request.id))
            if credential is None:
                raise UserNotFoundException(credential_id=request.id)
            await credential.delete()
            logger.success("Account with the id {} has been deleted.", request.id)
            return credential_pb2.Empty()
        except UserNotFoundException as error:
            return credential_pb2.Empty(error_message=error.message, error_code=error.code)
        except Exception:
            return credential_pb2.Empty(error_message="An error has occurred.", error_code=500)

    async def RefreshToken(self, request, context):
        """ Issues new access and refresh tokens.
            Input: Refresh token.
            Output: Access token, refresh token, or error. """
        try:
            payload = jwt.decode(request.refresh_token, JWT_REFRESH_SECRET, algorithms=["HS256"])
            credential = Credential.find_one(Credential.id == payload.get("id"))
            if credential is None:
                raise UserNotFoundException(credential_id=payload.get("id"))
            access_token = jwt.encode({
                "id": payload.get("id"),
                "role": payload.get("role"),
                "exp": datetime.utcnow() + timedelta(minutes=30)
            }, JWT_ACCESS_SECRET)
            refresh_token = jwt.encode({
                "id": payload.get("id"),
                "role": payload.get("role"),
                "exp": datetime.utcnow() + timedelta(days=7)
            }, JWT_REFRESH_SECRET)
            logger.success("Successfully issued new access and refresh tokens for user {}.", payload.get("id"))
            return credential_pb2.Token(access_token=access_token, refresh_token=refresh_token)
        except InvalidTokenError:
            return credential_pb2.Token(access_token="", error_message="Invalid refresh token.", error_code=498)
        except UserNotFoundException as error:
            return credential_pb2.Token(access_token="", error_message=error.message, error_code=error.code)

    async def CheckAuthority(self, request, context):
        """ Checks if user has the authority to perform an operation.
            Input: JWT access token.
            Output: Boolean, or error. """
        try:
            payload = jwt.decode(request.refresh_token, JWT_REFRESH_SECRET)
            credential_id = payload.get("id")
            credential = await Credential.find_one(Credential.id == credential_id)
            if credential is None:
                raise UserNotFoundException(credential_id=credential_id)
            if credential.role.value != request.role:
                raise UnauthorizedException(credential_id=credential_id)
            return credential_pb2.ValidateResponse(validated=True)
        except InvalidTokenError:
            return credential_pb2.ValidateResponse(validated=False, error_message="Invalid access token.",
                                                   error_code=498)
        except UserNotFoundException or UnauthorizedException as error:
            return credential_pb2.ValidateResponse(validated=False, error_message=error.message, error_code=error.code)
