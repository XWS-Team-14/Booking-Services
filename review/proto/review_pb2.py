# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: review.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0creview.proto\x12\x06review\"]\n\x05\x45mpty\x12\x1a\n\rerror_message\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code25\n\rReviewService\x12$\n\x04Send\x12\r.review.Empty\x1a\r.review.Emptyb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'review_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=24
  _EMPTY._serialized_end=117
  _REVIEWSERVICE._serialized_start=119
  _REVIEWSERVICE._serialized_end=172
# @@protoc_insertion_point(module_scope)
