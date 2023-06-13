import uuid
from datetime import datetime
from loguru import logger
from proto import orchestrator_pb2_grpc, orchestrator_pb2
from saga_orchestrator.app.models.log import Log
from saga_orchestrator.app.models.log_type import LogTypeEnum
from saga_orchestrator.app.models.operation import OperationEnum
from saga_orchestrator.app.models.status import StatusEnum
from saga_orchestrator.app.models.userId import UserId

class OrchestratorServicer(orchestrator_pb2_grpc.OrchestratorServicer):
    async def DeleteUser(self, request, context):
        logger.info(f'Recieved delete user {request.id} command')
        log = Log(
            id = uuid.UUID(),
            transaction_id = uuid.UUID(),
            log_type = LogTypeEnum.execute,
            timestamp = datetime.utcnow(),
            operation = OperationEnum.delete,
            target = "all",
            status = StatusEnum.sent,
            objects = UserId(user_id = request.id)
        )
        await log.insert()
        logger.info(f'Logged {log.transaction_id} transaction to database')
        #send out kafka messages
        return orchestrator_pb2.EmptyMessage(error_message = 'Accepted', error_code = 202 )