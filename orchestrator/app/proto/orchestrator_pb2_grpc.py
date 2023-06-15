# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import orchestrator_pb2 as orchestrator__pb2


class OrchestratorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DeleteUser = channel.unary_unary(
                '/Orchestrator/DeleteUser',
                request_serializer=orchestrator__pb2.UserId.SerializeToString,
                response_deserializer=orchestrator__pb2.EmptyMessage.FromString,
                )


class OrchestratorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrchestratorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=orchestrator__pb2.UserId.FromString,
                    response_serializer=orchestrator__pb2.EmptyMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Orchestrator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Orchestrator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Orchestrator/DeleteUser',
            orchestrator__pb2.UserId.SerializeToString,
            orchestrator__pb2.EmptyMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
