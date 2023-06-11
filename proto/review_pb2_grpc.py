# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import review_pb2 as review__pb2


class ReviewServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Send = channel.unary_unary(
                '/review.ReviewService/Send',
                request_serializer=review__pb2.Empty.SerializeToString,
                response_deserializer=review__pb2.Empty.FromString,
                )
        self.GetHostStatus = channel.unary_unary(
                '/review.ReviewService/GetHostStatus',
                request_serializer=review__pb2.HostId.SerializeToString,
                response_deserializer=review__pb2.HostStatus.FromString,
                )


class ReviewServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Send(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHostStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReviewServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Send': grpc.unary_unary_rpc_method_handler(
                    servicer.Send,
                    request_deserializer=review__pb2.Empty.FromString,
                    response_serializer=review__pb2.Empty.SerializeToString,
            ),
            'GetHostStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHostStatus,
                    request_deserializer=review__pb2.HostId.FromString,
                    response_serializer=review__pb2.HostStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'review.ReviewService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReviewService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Send(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/Send',
            review__pb2.Empty.SerializeToString,
            review__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHostStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetHostStatus',
            review__pb2.HostId.SerializeToString,
            review__pb2.HostStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
