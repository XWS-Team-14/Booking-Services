# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import availability_crud_pb2 as availability__crud__pb2


class AvailabilityCrudStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAll = channel.unary_unary(
                '/AvailabilityCrud/GetAll',
                request_serializer=availability__crud__pb2.Empty.SerializeToString,
                response_deserializer=availability__crud__pb2.AvailabilityDtos.FromString,
                )
        self.GetAllSearch = channel.unary_unary(
                '/AvailabilityCrud/GetAllSearch',
                request_serializer=availability__crud__pb2.SearchDetails.SerializeToString,
                response_deserializer=availability__crud__pb2.ExpandedAvailabilityDtos.FromString,
                )
        self.GetById = channel.unary_unary(
                '/AvailabilityCrud/GetById',
                request_serializer=availability__crud__pb2.AvailabilityId.SerializeToString,
                response_deserializer=availability__crud__pb2.AvailabilityDto.FromString,
                )
        self.Create = channel.unary_unary(
                '/AvailabilityCrud/Create',
                request_serializer=availability__crud__pb2.AvailabilityDto.SerializeToString,
                response_deserializer=availability__crud__pb2.Result.FromString,
                )
        self.Delete = channel.unary_unary(
                '/AvailabilityCrud/Delete',
                request_serializer=availability__crud__pb2.AvailabilityId.SerializeToString,
                response_deserializer=availability__crud__pb2.Result.FromString,
                )
        self.Update = channel.unary_unary(
                '/AvailabilityCrud/Update',
                request_serializer=availability__crud__pb2.AvailabilityDto.SerializeToString,
                response_deserializer=availability__crud__pb2.Result.FromString,
                )
        self.AddOccupiedInterval = channel.unary_unary(
                '/AvailabilityCrud/AddOccupiedInterval',
                request_serializer=availability__crud__pb2.UpdateIntervalDto.SerializeToString,
                response_deserializer=availability__crud__pb2.Result.FromString,
                )
        self.GetByAccommodationId = channel.unary_unary(
                '/AvailabilityCrud/GetByAccommodationId',
                request_serializer=availability__crud__pb2.AvailabilityId.SerializeToString,
                response_deserializer=availability__crud__pb2.AvailabilityDto.FromString,
                )


class AvailabilityCrudServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAll(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllSearch(self, request, context):
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

    def AddOccupiedInterval(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetByAccommodationId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AvailabilityCrudServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAll': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAll,
                    request_deserializer=availability__crud__pb2.Empty.FromString,
                    response_serializer=availability__crud__pb2.AvailabilityDtos.SerializeToString,
            ),
            'GetAllSearch': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllSearch,
                    request_deserializer=availability__crud__pb2.SearchDetails.FromString,
                    response_serializer=availability__crud__pb2.ExpandedAvailabilityDtos.SerializeToString,
            ),
            'GetById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetById,
                    request_deserializer=availability__crud__pb2.AvailabilityId.FromString,
                    response_serializer=availability__crud__pb2.AvailabilityDto.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=availability__crud__pb2.AvailabilityDto.FromString,
                    response_serializer=availability__crud__pb2.Result.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=availability__crud__pb2.AvailabilityId.FromString,
                    response_serializer=availability__crud__pb2.Result.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=availability__crud__pb2.AvailabilityDto.FromString,
                    response_serializer=availability__crud__pb2.Result.SerializeToString,
            ),
            'AddOccupiedInterval': grpc.unary_unary_rpc_method_handler(
                    servicer.AddOccupiedInterval,
                    request_deserializer=availability__crud__pb2.UpdateIntervalDto.FromString,
                    response_serializer=availability__crud__pb2.Result.SerializeToString,
            ),
            'GetByAccommodationId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByAccommodationId,
                    request_deserializer=availability__crud__pb2.AvailabilityId.FromString,
                    response_serializer=availability__crud__pb2.AvailabilityDto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AvailabilityCrud', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AvailabilityCrud(object):
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
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/GetAll',
            availability__crud__pb2.Empty.SerializeToString,
            availability__crud__pb2.AvailabilityDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllSearch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/GetAllSearch',
            availability__crud__pb2.SearchDetails.SerializeToString,
            availability__crud__pb2.ExpandedAvailabilityDtos.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/GetById',
            availability__crud__pb2.AvailabilityId.SerializeToString,
            availability__crud__pb2.AvailabilityDto.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/Create',
            availability__crud__pb2.AvailabilityDto.SerializeToString,
            availability__crud__pb2.Result.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/Delete',
            availability__crud__pb2.AvailabilityId.SerializeToString,
            availability__crud__pb2.Result.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/Update',
            availability__crud__pb2.AvailabilityDto.SerializeToString,
            availability__crud__pb2.Result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddOccupiedInterval(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/AddOccupiedInterval',
            availability__crud__pb2.UpdateIntervalDto.SerializeToString,
            availability__crud__pb2.Result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetByAccommodationId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AvailabilityCrud/GetByAccommodationId',
            availability__crud__pb2.AvailabilityId.SerializeToString,
            availability__crud__pb2.AvailabilityDto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
