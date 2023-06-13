import uuid
from datetime import datetime
from loguru import logger
from proto import orchestrator_pb2_grpc, orchestrator_pb2
from app.models.log import Log
from app.models.log_type import LogTypeEnum
from app.models.operation import OperationEnum
from app.models.status import StatusEnum
from app.models.userId import UserId

class OrchestratorServicer(orchestrator_pb2_grpc.OrchestratorServicer):
    async def DeleteUser(self, request, context):
        logger.info(f'Recieved delete user {request.id} command')
        try:
            log = Log(
                id = uuid.uuid4(),
                transaction_id = uuid.uuid4(),
                log_type = LogTypeEnum.execute,
                timestamp = datetime.utcnow(),
                operation = OperationEnum.delete,
                target = "all",
                status = StatusEnum.sent,
                objects = request.id
            )
            logger.info(log)
            await log.insert()
            logger.info(f'Logged {log.transaction_id} transaction to database')
        except Exception as e:
            logger.info(e)  
        #send out kafka messages
        return orchestrator_pb2.EmptyMessage(error_message = 'Accepted', error_code = 202 )