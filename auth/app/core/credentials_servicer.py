from loguru import logger
from passlib.hash import bcrypt

from proto import credential_pb2, credential_pb2_grpc
from ..models.credential import Credential


class CredentialServicer(credential_pb2_grpc.CredentialServiceServicer):
    async def Create(self, request, context):
        logger.info('Request received')
        try:
            credential = Credential(email=request.email, password=bcrypt.hash(request.password))
            await credential.insert()
            return credential_pb2.Empty()
        except:
            logger.catch()
