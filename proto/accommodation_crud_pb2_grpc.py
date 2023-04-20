# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import accommodation_crud_pb2 as accommodation__crud__pb2


class AccommodationCrudStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAll = channel.unary_unary(
                '/AccommodationCrud/GetAll',
                request_serializer=accommodation__crud__pb2.Empty.SerializeToString,
                response_deserializer=accommodation__crud__pb2.Accommodations.FromString,
                )
        self.GetById = channel.unary_unary(
                '/AccommodationCrud/GetById',
                request_serializer=accommodation__crud__pb2.AccommodationId.SerializeToString,
                response_deserializer=accommodation__crud__pb2.Accommodation.FromString,
                )
        self.Create = channel.unary_unary(
                '/AccommodationCrud/Create',
                request_serializer=accommodation__crud__pb2.Accommodation.SerializeToString,
                response_deserializer=accommodation__crud__pb2.Empty.FromString,
                )
        self.Delete = channel.unary_unary(
                '/AccommodationCrud/Delete',
                request_serializer=accommodation__crud__pb2.AccommodationId.SerializeToString,
                response_deserializer=accommodation__crud__pb2.Empty.FromString,
                )
        self.Update = channel.unary_unary(
                '/AccommodationCrud/Update',
                request_serializer=accommodation__crud__pb2.Accommodation.SerializeToString,
                response_deserializer=accommodation__crud__pb2.Empty.FromString,
                )


class AccommodationCrudServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAll(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AccommodationCrudServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAll': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAll,
                    request_deserializer=accommodation__crud__pb2.Empty.FromString,
                    response_serializer=accommodation__crud__pb2.Accommodations.SerializeToString,
            ),
            'GetById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetById,
                    request_deserializer=accommodation__crud__pb2.AccommodationId.FromString,
                    response_serializer=accommodation__crud__pb2.Accommodation.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=accommodation__crud__pb2.Accommodation.FromString,
                    response_serializer=accommodation__crud__pb2.Empty.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=accommodation__crud__pb2.AccommodationId.FromString,
                    response_serializer=accommodation__crud__pb2.Empty.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=accommodation__crud__pb2.Accommodation.FromString,
                    response_serializer=accommodation__crud__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AccommodationCrud', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AccommodationCrud(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAll(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AccommodationCrud/GetAll',
            accommodation__crud__pb2.Empty.SerializeToString,
            accommodation__crud__pb2.Accommodations.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AccommodationCrud/GetById',
            accommodation__crud__pb2.AccommodationId.SerializeToString,
            accommodation__crud__pb2.Accommodation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AccommodationCrud/Create',
            accommodation__crud__pb2.Accommodation.SerializeToString,
            accommodation__crud__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AccommodationCrud/Delete',
            accommodation__crud__pb2.AccommodationId.SerializeToString,
            accommodation__crud__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AccommodationCrud/Update',
            accommodation__crud__pb2.Accommodation.SerializeToString,
            accommodation__crud__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
