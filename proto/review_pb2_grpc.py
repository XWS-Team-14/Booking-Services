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
        self.CreateReview = channel.unary_unary(
                '/review.ReviewService/CreateReview',
                request_serializer=review__pb2.Review.SerializeToString,
                response_deserializer=review__pb2.AverageRatings.FromString,
                )
        self.GetAllReviews = channel.unary_unary(
                '/review.ReviewService/GetAllReviews',
                request_serializer=review__pb2.Empty.SerializeToString,
                response_deserializer=review__pb2.ReviewDtos.FromString,
                )
        self.GetReviewById = channel.unary_unary(
                '/review.ReviewService/GetReviewById',
                request_serializer=review__pb2.ReviewId.SerializeToString,
                response_deserializer=review__pb2.Review.FromString,
                )
        self.GetReviewsByHost = channel.unary_unary(
                '/review.ReviewService/GetReviewsByHost',
                request_serializer=review__pb2.HostId.SerializeToString,
                response_deserializer=review__pb2.ReviewDtos.FromString,
                )
        self.UpdateReview = channel.unary_unary(
                '/review.ReviewService/UpdateReview',
                request_serializer=review__pb2.UpdateReviewDto.SerializeToString,
                response_deserializer=review__pb2.AverageRatings.FromString,
                )
        self.DeleteReview = channel.unary_unary(
                '/review.ReviewService/DeleteReview',
                request_serializer=review__pb2.ReviewId.SerializeToString,
                response_deserializer=review__pb2.AverageRatings.FromString,
                )
        self.GetReviewsByPoster = channel.unary_unary(
                '/review.ReviewService/GetReviewsByPoster',
                request_serializer=review__pb2.Poster.SerializeToString,
                response_deserializer=review__pb2.ReviewDtos.FromString,
                )
        self.GetAllAccommodationsWithFeaturedHost = channel.unary_unary(
                '/review.ReviewService/GetAllAccommodationsWithFeaturedHost',
                request_serializer=review__pb2.Empty.SerializeToString,
                response_deserializer=review__pb2.Accommodations.FromString,
                )
        self.GetReviewsByAccommodation = channel.unary_unary(
                '/review.ReviewService/GetReviewsByAccommodation',
                request_serializer=review__pb2.AccommodationId.SerializeToString,
                response_deserializer=review__pb2.ReviewDtos.FromString,
                )
        self.CreateHostAndAccommodation = channel.unary_unary(
                '/review.ReviewService/CreateHostAndAccommodation',
                request_serializer=review__pb2.HostAccommodation.SerializeToString,
                response_deserializer=review__pb2.Empty.FromString,
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

    def CreateReview(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllReviews(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReviewById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReviewsByHost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateReview(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteReview(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReviewsByPoster(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllAccommodationsWithFeaturedHost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReviewsByAccommodation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateHostAndAccommodation(self, request, context):
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
            'CreateReview': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateReview,
                    request_deserializer=review__pb2.Review.FromString,
                    response_serializer=review__pb2.AverageRatings.SerializeToString,
            ),
            'GetAllReviews': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllReviews,
                    request_deserializer=review__pb2.Empty.FromString,
                    response_serializer=review__pb2.ReviewDtos.SerializeToString,
            ),
            'GetReviewById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReviewById,
                    request_deserializer=review__pb2.ReviewId.FromString,
                    response_serializer=review__pb2.Review.SerializeToString,
            ),
            'GetReviewsByHost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReviewsByHost,
                    request_deserializer=review__pb2.HostId.FromString,
                    response_serializer=review__pb2.ReviewDtos.SerializeToString,
            ),
            'UpdateReview': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateReview,
                    request_deserializer=review__pb2.UpdateReviewDto.FromString,
                    response_serializer=review__pb2.AverageRatings.SerializeToString,
            ),
            'DeleteReview': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteReview,
                    request_deserializer=review__pb2.ReviewId.FromString,
                    response_serializer=review__pb2.AverageRatings.SerializeToString,
            ),
            'GetReviewsByPoster': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReviewsByPoster,
                    request_deserializer=review__pb2.Poster.FromString,
                    response_serializer=review__pb2.ReviewDtos.SerializeToString,
            ),
            'GetAllAccommodationsWithFeaturedHost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllAccommodationsWithFeaturedHost,
                    request_deserializer=review__pb2.Empty.FromString,
                    response_serializer=review__pb2.Accommodations.SerializeToString,
            ),
            'GetReviewsByAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReviewsByAccommodation,
                    request_deserializer=review__pb2.AccommodationId.FromString,
                    response_serializer=review__pb2.ReviewDtos.SerializeToString,
            ),
            'CreateHostAndAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateHostAndAccommodation,
                    request_deserializer=review__pb2.HostAccommodation.FromString,
                    response_serializer=review__pb2.Empty.SerializeToString,
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

    @staticmethod
    def CreateReview(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/CreateReview',
            review__pb2.Review.SerializeToString,
            review__pb2.AverageRatings.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllReviews(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetAllReviews',
            review__pb2.Empty.SerializeToString,
            review__pb2.ReviewDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReviewById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetReviewById',
            review__pb2.ReviewId.SerializeToString,
            review__pb2.Review.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReviewsByHost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetReviewsByHost',
            review__pb2.HostId.SerializeToString,
            review__pb2.ReviewDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateReview(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/UpdateReview',
            review__pb2.UpdateReviewDto.SerializeToString,
            review__pb2.AverageRatings.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteReview(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/DeleteReview',
            review__pb2.ReviewId.SerializeToString,
            review__pb2.AverageRatings.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReviewsByPoster(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetReviewsByPoster',
            review__pb2.Poster.SerializeToString,
            review__pb2.ReviewDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllAccommodationsWithFeaturedHost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetAllAccommodationsWithFeaturedHost',
            review__pb2.Empty.SerializeToString,
            review__pb2.Accommodations.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReviewsByAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/GetReviewsByAccommodation',
            review__pb2.AccommodationId.SerializeToString,
            review__pb2.ReviewDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateHostAndAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/review.ReviewService/CreateHostAndAccommodation',
            review__pb2.HostAccommodation.SerializeToString,
            review__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
