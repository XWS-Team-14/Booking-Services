# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: orchestrator.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12orchestrator.proto\"d\n\x0c\x45mptyMessage\x12\x1a\n\rerror_message\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code\"\x14\n\x06UserId\x12\n\n\x02id\x18\x01 \x01(\t24\n\x0cOrchestrator\x12$\n\nDeleteUser\x12\x07.UserId\x1a\r.EmptyMessageb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'orchestrator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTYMESSAGE._serialized_start=22
  _EMPTYMESSAGE._serialized_end=122
  _USERID._serialized_start=124
  _USERID._serialized_end=144
  _ORCHESTRATOR._serialized_start=146
  _ORCHESTRATOR._serialized_end=198
# @@protoc_insertion_point(module_scope)
