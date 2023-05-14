# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import reservation_crud_pb2 as reservation__crud__pb2


class ReservationCrudStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAll = channel.unary_unary(
                '/ReservationCrud/GetAll',
                request_serializer=reservation__crud__pb2.NoParameter.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetById = channel.unary_unary(
                '/ReservationCrud/GetById',
                request_serializer=reservation__crud__pb2.ReservationId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDto.FromString,
                )
        self.Create = channel.unary_unary(
                '/ReservationCrud/Create',
                request_serializer=reservation__crud__pb2.ReservationDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.Delete = channel.unary_unary(
                '/ReservationCrud/Delete',
                request_serializer=reservation__crud__pb2.ReservationId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.Update = channel.unary_unary(
                '/ReservationCrud/Update',
                request_serializer=reservation__crud__pb2.ReservationDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.GetByHost = channel.unary_unary(
                '/ReservationCrud/GetByHost',
                request_serializer=reservation__crud__pb2.HostId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetByGuest = channel.unary_unary(
                '/ReservationCrud/GetByGuest',
                request_serializer=reservation__crud__pb2.GuestId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetReservationsForAcceptance = channel.unary_unary(
                '/ReservationCrud/GetReservationsForAcceptance',
                request_serializer=reservation__crud__pb2.ReservationDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.AcceptReservation = channel.unary_unary(
                '/ReservationCrud/AcceptReservation',
                request_serializer=reservation__crud__pb2.ReservationDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.GetPendingReservationsByHost = channel.unary_unary(
                '/ReservationCrud/GetPendingReservationsByHost',
                request_serializer=reservation__crud__pb2.HostId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetActiveByGuest = channel.unary_unary(
                '/ReservationCrud/GetActiveByGuest',
                request_serializer=reservation__crud__pb2.GuestId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetActiveByHost = channel.unary_unary(
                '/ReservationCrud/GetActiveByHost',
                request_serializer=reservation__crud__pb2.HostId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )
        self.GetGuestById = channel.unary_unary(
                '/ReservationCrud/GetGuestById',
                request_serializer=reservation__crud__pb2.GuestId.SerializeToString,
                response_deserializer=reservation__crud__pb2.Guest.FromString,
                )
        self.CreateGuest = channel.unary_unary(
                '/ReservationCrud/CreateGuest',
                request_serializer=reservation__crud__pb2.Guest.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.DeleteGuest = channel.unary_unary(
                '/ReservationCrud/DeleteGuest',
                request_serializer=reservation__crud__pb2.GuestId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.UpdateGuest = channel.unary_unary(
                '/ReservationCrud/UpdateGuest',
                request_serializer=reservation__crud__pb2.Guest.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.GetAllGuests = channel.unary_unary(
                '/ReservationCrud/GetAllGuests',
                request_serializer=reservation__crud__pb2.NoParameter.SerializeToString,
                response_deserializer=reservation__crud__pb2.Guests.FromString,
                )
        self.CreateAccommodation = channel.unary_unary(
                '/ReservationCrud/CreateAccommodation',
                request_serializer=reservation__crud__pb2.AccommodationResDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.UpdateAccommodation = channel.unary_unary(
                '/ReservationCrud/UpdateAccommodation',
                request_serializer=reservation__crud__pb2.AccommodationResDto.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.DeleteAccommodation = channel.unary_unary(
                '/ReservationCrud/DeleteAccommodation',
                request_serializer=reservation__crud__pb2.AccommodationResId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationResult.FromString,
                )
        self.GetAccommodationById = channel.unary_unary(
                '/ReservationCrud/GetAccommodationById',
                request_serializer=reservation__crud__pb2.AccommodationResId.SerializeToString,
                response_deserializer=reservation__crud__pb2.AccommodationResDto.FromString,
                )
        self.GetReservationsByAccommodation = channel.unary_unary(
                '/ReservationCrud/GetReservationsByAccommodation',
                request_serializer=reservation__crud__pb2.AccommodationResId.SerializeToString,
                response_deserializer=reservation__crud__pb2.ReservationDtos.FromString,
                )


class ReservationCrudServicer(object):
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

    def GetByHost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetByGuest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReservationsForAcceptance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AcceptReservation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPendingReservationsByHost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetActiveByGuest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetActiveByHost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGuestById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateGuest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteGuest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateGuest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllGuests(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccommodation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAccommodation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAccommodation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccommodationById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReservationsByAccommodation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReservationCrudServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAll': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAll,
                    request_deserializer=reservation__crud__pb2.NoParameter.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetById,
                    request_deserializer=reservation__crud__pb2.ReservationId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDto.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=reservation__crud__pb2.ReservationDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=reservation__crud__pb2.ReservationId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=reservation__crud__pb2.ReservationDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'GetByHost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByHost,
                    request_deserializer=reservation__crud__pb2.HostId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetByGuest': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByGuest,
                    request_deserializer=reservation__crud__pb2.GuestId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetReservationsForAcceptance': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReservationsForAcceptance,
                    request_deserializer=reservation__crud__pb2.ReservationDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'AcceptReservation': grpc.unary_unary_rpc_method_handler(
                    servicer.AcceptReservation,
                    request_deserializer=reservation__crud__pb2.ReservationDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'GetPendingReservationsByHost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPendingReservationsByHost,
                    request_deserializer=reservation__crud__pb2.HostId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetActiveByGuest': grpc.unary_unary_rpc_method_handler(
                    servicer.GetActiveByGuest,
                    request_deserializer=reservation__crud__pb2.GuestId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetActiveByHost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetActiveByHost,
                    request_deserializer=reservation__crud__pb2.HostId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
            'GetGuestById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGuestById,
                    request_deserializer=reservation__crud__pb2.GuestId.FromString,
                    response_serializer=reservation__crud__pb2.Guest.SerializeToString,
            ),
            'CreateGuest': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateGuest,
                    request_deserializer=reservation__crud__pb2.Guest.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'DeleteGuest': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteGuest,
                    request_deserializer=reservation__crud__pb2.GuestId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'UpdateGuest': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateGuest,
                    request_deserializer=reservation__crud__pb2.Guest.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'GetAllGuests': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllGuests,
                    request_deserializer=reservation__crud__pb2.NoParameter.FromString,
                    response_serializer=reservation__crud__pb2.Guests.SerializeToString,
            ),
            'CreateAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccommodation,
                    request_deserializer=reservation__crud__pb2.AccommodationResDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'UpdateAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAccommodation,
                    request_deserializer=reservation__crud__pb2.AccommodationResDto.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'DeleteAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteAccommodation,
                    request_deserializer=reservation__crud__pb2.AccommodationResId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationResult.SerializeToString,
            ),
            'GetAccommodationById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccommodationById,
                    request_deserializer=reservation__crud__pb2.AccommodationResId.FromString,
                    response_serializer=reservation__crud__pb2.AccommodationResDto.SerializeToString,
            ),
            'GetReservationsByAccommodation': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReservationsByAccommodation,
                    request_deserializer=reservation__crud__pb2.AccommodationResId.FromString,
                    response_serializer=reservation__crud__pb2.ReservationDtos.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ReservationCrud', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReservationCrud(object):
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
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetAll',
            reservation__crud__pb2.NoParameter.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetById',
            reservation__crud__pb2.ReservationId.SerializeToString,
            reservation__crud__pb2.ReservationDto.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/Create',
            reservation__crud__pb2.ReservationDto.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/Delete',
            reservation__crud__pb2.ReservationId.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/Update',
            reservation__crud__pb2.ReservationDto.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetByHost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetByHost',
            reservation__crud__pb2.HostId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetByGuest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetByGuest',
            reservation__crud__pb2.GuestId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReservationsForAcceptance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetReservationsForAcceptance',
            reservation__crud__pb2.ReservationDto.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AcceptReservation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/AcceptReservation',
            reservation__crud__pb2.ReservationDto.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPendingReservationsByHost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetPendingReservationsByHost',
            reservation__crud__pb2.HostId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetActiveByGuest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetActiveByGuest',
            reservation__crud__pb2.GuestId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetActiveByHost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetActiveByHost',
            reservation__crud__pb2.HostId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGuestById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetGuestById',
            reservation__crud__pb2.GuestId.SerializeToString,
            reservation__crud__pb2.Guest.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateGuest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/CreateGuest',
            reservation__crud__pb2.Guest.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteGuest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/DeleteGuest',
            reservation__crud__pb2.GuestId.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateGuest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/UpdateGuest',
            reservation__crud__pb2.Guest.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllGuests(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetAllGuests',
            reservation__crud__pb2.NoParameter.SerializeToString,
            reservation__crud__pb2.Guests.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/CreateAccommodation',
            reservation__crud__pb2.AccommodationResDto.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/UpdateAccommodation',
            reservation__crud__pb2.AccommodationResDto.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/DeleteAccommodation',
            reservation__crud__pb2.AccommodationResId.SerializeToString,
            reservation__crud__pb2.ReservationResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccommodationById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetAccommodationById',
            reservation__crud__pb2.AccommodationResId.SerializeToString,
            reservation__crud__pb2.AccommodationResDto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReservationsByAccommodation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReservationCrud/GetReservationsByAccommodation',
            reservation__crud__pb2.AccommodationResId.SerializeToString,
            reservation__crud__pb2.ReservationDtos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
