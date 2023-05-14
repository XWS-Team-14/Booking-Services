# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reservation_crud.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16reservation_crud.proto\"\r\n\x0bNoParameter\"#\n\x11ReservationResult\x12\x0e\n\x06status\x18\x01 \x01(\t\"\xe9\x01\n\x0eReservationDto\x12\x16\n\x0ereservation_id\x18\x01 \x01(\t\x12+\n\raccommodation\x18\x02 \x01(\x0b\x32\x14.AccommodationResDto\x12\x0f\n\x07host_id\x18\x03 \x01(\t\x12\x15\n\x05guest\x18\x04 \x01(\x0b\x32\x06.Guest\x12\x18\n\x10number_of_guests\x18\x05 \x01(\x05\x12\x16\n\x0e\x62\x65ginning_date\x18\x06 \x01(\t\x12\x13\n\x0b\x65nding_date\x18\x07 \x01(\t\x12\x13\n\x0btotal_price\x18\x08 \x01(\x01\x12\x0e\n\x06status\x18\t \x01(\x05\"1\n\x0fReservationDtos\x12\x1e\n\x05items\x18\x01 \x03(\x0b\x32\x0f.ReservationDto\"\x1b\n\rReservationId\x12\n\n\x02id\x18\x01 \x01(\t\"\x14\n\x06HostId\x12\n\n\x02id\x18\x01 \x01(\t\"1\n\x05Guest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1c\n\x14\x63\x61nceledReservations\x18\x02 \x01(\x05\"\x1f\n\x06Guests\x12\x15\n\x05items\x18\x01 \x03(\x0b\x32\x06.Guest\"\x15\n\x07GuestId\x12\n\n\x02id\x18\x01 \x01(\t\":\n\x13\x41\x63\x63ommodationResDto\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\x0f\x61utomaticAccept\x18\x02 \x01(\x08\" \n\x12\x41\x63\x63ommodationResId\x12\n\n\x02id\x18\x01 \x01(\t2\xf5\x08\n\x0fReservationCrud\x12(\n\x06GetAll\x12\x0c.NoParameter\x1a\x10.ReservationDtos\x12*\n\x07GetById\x12\x0e.ReservationId\x1a\x0f.ReservationDto\x12-\n\x06\x43reate\x12\x0f.ReservationDto\x1a\x12.ReservationResult\x12,\n\x06\x44\x65lete\x12\x0e.ReservationId\x1a\x12.ReservationResult\x12-\n\x06Update\x12\x0f.ReservationDto\x1a\x12.ReservationResult\x12&\n\tGetByHost\x12\x07.HostId\x1a\x10.ReservationDtos\x12(\n\nGetByGuest\x12\x08.GuestId\x1a\x10.ReservationDtos\x12\x41\n\x1cGetReservationsForAcceptance\x12\x0f.ReservationDto\x1a\x10.ReservationDtos\x12\x38\n\x11\x41\x63\x63\x65ptReservation\x12\x0f.ReservationDto\x1a\x12.ReservationResult\x12\x39\n\x1cGetPendingReservationsByHost\x12\x07.HostId\x1a\x10.ReservationDtos\x12.\n\x10GetActiveByGuest\x12\x08.GuestId\x1a\x10.ReservationDtos\x12,\n\x0fGetActiveByHost\x12\x07.HostId\x1a\x10.ReservationDtos\x12 \n\x0cGetGuestById\x12\x08.GuestId\x1a\x06.Guest\x12)\n\x0b\x43reateGuest\x12\x06.Guest\x1a\x12.ReservationResult\x12+\n\x0b\x44\x65leteGuest\x12\x08.GuestId\x1a\x12.ReservationResult\x12)\n\x0bUpdateGuest\x12\x06.Guest\x1a\x12.ReservationResult\x12%\n\x0cGetAllGuests\x12\x0c.NoParameter\x1a\x07.Guests\x12?\n\x13\x43reateAccommodation\x12\x14.AccommodationResDto\x1a\x12.ReservationResult\x12?\n\x13UpdateAccommodation\x12\x14.AccommodationResDto\x1a\x12.ReservationResult\x12>\n\x13\x44\x65leteAccommodation\x12\x13.AccommodationResId\x1a\x12.ReservationResult\x12\x41\n\x14GetAccommodationById\x12\x13.AccommodationResId\x1a\x14.AccommodationResDto\x12G\n\x1eGetReservationsByAccommodation\x12\x13.AccommodationResId\x1a\x10.ReservationDtosb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'reservation_crud_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NOPARAMETER._serialized_start=26
  _NOPARAMETER._serialized_end=39
  _RESERVATIONRESULT._serialized_start=41
  _RESERVATIONRESULT._serialized_end=76
  _RESERVATIONDTO._serialized_start=79
  _RESERVATIONDTO._serialized_end=312
  _RESERVATIONDTOS._serialized_start=314
  _RESERVATIONDTOS._serialized_end=363
  _RESERVATIONID._serialized_start=365
  _RESERVATIONID._serialized_end=392
  _HOSTID._serialized_start=394
  _HOSTID._serialized_end=414
  _GUEST._serialized_start=416
  _GUEST._serialized_end=465
  _GUESTS._serialized_start=467
  _GUESTS._serialized_end=498
  _GUESTID._serialized_start=500
  _GUESTID._serialized_end=521
  _ACCOMMODATIONRESDTO._serialized_start=523
  _ACCOMMODATIONRESDTO._serialized_end=581
  _ACCOMMODATIONRESID._serialized_start=583
  _ACCOMMODATIONRESID._serialized_end=615
  _RESERVATIONCRUD._serialized_start=618
  _RESERVATIONCRUD._serialized_end=1759
# @@protoc_insertion_point(module_scope)
