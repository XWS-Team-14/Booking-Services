# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: search.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csearch.proto\x12\x06search\":\n\x08Location\x12\x0f\n\x07\x63ountry\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\"j\n\x0cSearchParams\x12\"\n\x08location\x18\x01 \x01(\x0b\x32\x10.search.Location\x12\x0e\n\x06guests\x18\x02 \x01(\x05\x12&\n\x07\x64\x65tails\x18\x03 \x01(\x0b\x32\x15.search.SearchDetails\"\xfb\x01\n\rSearchResults\x12\x16\n\x0ereservation_id\x18\x01 \x01(\t\x12\x18\n\x10\x61\x63\x63ommodation_id\x18\x02 \x01(\t\x12\x0f\n\x07host_id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\"\n\x08location\x18\x05 \x01(\x0b\x32\x10.search.Location\x12\x10\n\x08\x66\x65\x61tures\x18\x06 \x03(\t\x12\x12\n\nimage_urls\x18\x07 \x03(\t\x12\x12\n\nmin_guests\x18\x08 \x01(\x05\x12\x12\n\nmax_guests\x18\t \x01(\x05\x12\x12\n\nbase_price\x18\n \x01(\x01\x12\x13\n\x0btotal_price\x18\x0b \x01(\x01\"J\n\rSearchDetails\x12\"\n\x08interval\x18\x01 \x01(\x0b\x32\x10.search.Interval\x12\x15\n\rnum_of_guests\x18\x02 \x01(\x05\"0\n\x08Interval\x12\x12\n\ndate_start\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61te_end\x18\x02 \x01(\t2J\n\x11\x41\x63\x63ommodationCrud\x12\x35\n\x06Search\x12\x14.search.SearchParams\x1a\x15.search.SearchResultsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'search_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOCATION._serialized_start=24
  _LOCATION._serialized_end=82
  _SEARCHPARAMS._serialized_start=84
  _SEARCHPARAMS._serialized_end=190
  _SEARCHRESULTS._serialized_start=193
  _SEARCHRESULTS._serialized_end=444
  _SEARCHDETAILS._serialized_start=446
  _SEARCHDETAILS._serialized_end=520
  _INTERVAL._serialized_start=522
  _INTERVAL._serialized_end=570
  _ACCOMMODATIONCRUD._serialized_start=572
  _ACCOMMODATIONCRUD._serialized_end=646
# @@protoc_insertion_point(module_scope)