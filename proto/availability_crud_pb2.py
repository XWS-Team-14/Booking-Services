# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: availability_crud.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x61vailability_crud.proto\"\x07\n\x05\x45mpty\"\x18\n\x06Result\x12\x0e\n\x06status\x18\x01 \x01(\t\"b\n\rSearchDetails\x12\x1b\n\x08interval\x18\x01 \x01(\x0b\x32\t.Interval\x12\x0e\n\x06guests\x18\x02 \x01(\x05\x12\x11\n\tprice_min\x18\x03 \x01(\x02\x12\x11\n\tprice_max\x18\x04 \x01(\x02\"<\n\x11UpdateIntervalDto\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1b\n\x08interval\x18\x02 \x01(\x0b\x32\t.Interval\"\x1c\n\x0e\x41vailabilityId\x12\n\n\x02id\x18\x01 \x01(\t\"7\n\x0eSpecialPricing\x12\r\n\x05title\x18\x01 \x01(\t\x12\x16\n\x0epricing_markup\x18\x02 \x01(\x01\"0\n\x08Interval\x12\x12\n\ndate_start\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61te_end\x18\x02 \x01(\t\"\xdc\x01\n\x0f\x41vailabilityDto\x12\x17\n\x0f\x61vailability_id\x18\x01 \x01(\t\x12\x18\n\x10\x61\x63\x63ommodation_id\x18\x02 \x01(\t\x12\x1b\n\x08interval\x18\x03 \x01(\x0b\x32\t.Interval\x12\x14\n\x0cpricing_type\x18\x04 \x01(\t\x12\x12\n\nbase_price\x18\x05 \x01(\x01\x12(\n\x0fspecial_pricing\x18\x06 \x03(\x0b\x32\x0f.SpecialPricing\x12%\n\x12occupied_intervals\x18\x07 \x03(\x0b\x32\t.Interval\"\xf9\x01\n\x17\x45xpandedAvailabilityDto\x12\x17\n\x0f\x61vailability_id\x18\x01 \x01(\t\x12\x18\n\x10\x61\x63\x63ommodation_id\x18\x02 \x01(\t\x12\x1b\n\x08interval\x18\x03 \x01(\x0b\x32\t.Interval\x12\x14\n\x0cpricing_type\x18\x04 \x01(\t\x12\x12\n\nbase_price\x18\x05 \x01(\x01\x12\x13\n\x0btotal_price\x18\x06 \x01(\x01\x12(\n\x0fspecial_pricing\x18\x07 \x03(\x0b\x32\x0f.SpecialPricing\x12%\n\x12occupied_intervals\x18\x08 \x03(\x0b\x32\t.Interval\"3\n\x10\x41vailabilityDtos\x12\x1f\n\x05items\x18\x01 \x03(\x0b\x32\x10.AvailabilityDto\"C\n\x18\x45xpandedAvailabilityDtos\x12\'\n\x05items\x18\x01 \x03(\x0b\x32\x18.ExpandedAvailabilityDto\"\x16\n\x05Price\x12\r\n\x05price\x18\x01 \x01(\x01\"T\n\x0bPriceLookup\x12\x1b\n\x08interval\x18\x01 \x01(\x0b\x32\t.Interval\x12\x0e\n\x06guests\x18\x02 \x01(\x05\x12\x18\n\x10\x61\x63\x63ommodation_id\x18\x03 \x01(\t2\xd6\x03\n\x10\x41vailabilityCrud\x12#\n\x06GetAll\x12\x06.Empty\x1a\x11.AvailabilityDtos\x12\x39\n\x0cGetAllSearch\x12\x0e.SearchDetails\x1a\x19.ExpandedAvailabilityDtos\x12,\n\x07GetById\x12\x0f.AvailabilityId\x1a\x10.AvailabilityDto\x12#\n\x06\x43reate\x12\x10.AvailabilityDto\x1a\x07.Result\x12\"\n\x06\x44\x65lete\x12\x0f.AvailabilityId\x1a\x07.Result\x12#\n\x06Update\x12\x10.AvailabilityDto\x1a\x07.Result\x12\x32\n\x13\x41\x64\x64OccupiedInterval\x12\x12.UpdateIntervalDto\x1a\x07.Result\x12\x35\n\x16RemoveOccupiedInterval\x12\x12.UpdateIntervalDto\x1a\x07.Result\x12\x39\n\x14GetByAccommodationId\x12\x0f.AvailabilityId\x1a\x10.AvailabilityDto\x12 \n\x08GetPrice\x12\x0c.PriceLookup\x1a\x06.Priceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'availability_crud_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=27
  _EMPTY._serialized_end=34
  _RESULT._serialized_start=36
  _RESULT._serialized_end=60
  _SEARCHDETAILS._serialized_start=62
  _SEARCHDETAILS._serialized_end=160
  _UPDATEINTERVALDTO._serialized_start=162
  _UPDATEINTERVALDTO._serialized_end=222
  _AVAILABILITYID._serialized_start=224
  _AVAILABILITYID._serialized_end=252
  _SPECIALPRICING._serialized_start=254
  _SPECIALPRICING._serialized_end=309
  _INTERVAL._serialized_start=311
  _INTERVAL._serialized_end=359
  _AVAILABILITYDTO._serialized_start=362
  _AVAILABILITYDTO._serialized_end=582
  _EXPANDEDAVAILABILITYDTO._serialized_start=585
  _EXPANDEDAVAILABILITYDTO._serialized_end=834
  _AVAILABILITYDTOS._serialized_start=836
  _AVAILABILITYDTOS._serialized_end=887
  _EXPANDEDAVAILABILITYDTOS._serialized_start=889
  _EXPANDEDAVAILABILITYDTOS._serialized_end=956
  _PRICE._serialized_start=958
  _PRICE._serialized_end=980
  _PRICELOOKUP._serialized_start=982
  _PRICELOOKUP._serialized_end=1066
  _AVAILABILITYCRUD._serialized_start=1069
  _AVAILABILITYCRUD._serialized_end=1539
# @@protoc_insertion_point(module_scope)
