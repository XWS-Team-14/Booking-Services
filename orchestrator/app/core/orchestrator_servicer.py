import uuid
from datetime import datetime
from loguru import logger
import grpc
from proto import orchestrator_pb2_grpc, orchestrator_pb2
from app.models.log import Log
from app.models.log_type import LogTypeEnum
from app.models.operation import OperationEnum
from app.models.status import StatusEnum
from app.models.userId import UserId
from app.constants import kafka_producer, kafka_server, accommodation_server
from google.protobuf.json_format import MessageToDict, Parse
from app.models.accommodations_shema import(
    ResponseAccommodations
)


from proto import (
    accommodation_pb2,
    accommodation_pb2_grpc
    )

class OrchestratorServicer(orchestrator_pb2_grpc.OrchestratorServicer):
    async def DeleteUser(self, request, context):
        logger.info(f'Recieved delete user {request.id} command')
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
        
        #fetch accommodation id's via grpc - suboptimal if I have the time it will be upgraded
        
        async with grpc.aio.insecure_channel(accommodation_server) as channel:
            stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
            dto = accommodation_pb2.InputId(
                id=request.id,
            )
            response = await stub.GetByUser(dto)

        accomomodations = ResponseAccommodations.parse_obj(
            MessageToDict(response, preserving_proto_field_name=True)
        )
        logger.info(accomomodations)
        accomomodation_ids = []
        for item in accomomodations.items:
            accomomodation_ids.append(str(item.host_id))
        
        logger.info(accomomodation_ids)
        #send out kafka messages
        kafka_producer.send('user-delete', {
            'user': str(request.id),
        })
        kafka_producer.send('accommodation-delete', {
            'user': str(request.id),
        })
        kafka_producer.send('availability-delete', accomomodation_ids)
        return orchestrator_pb2.EmptyMessage(error_message = 'Accepted', error_code = 202 )