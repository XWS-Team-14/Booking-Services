# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04user\"d\n\x0c\x45mptyMessage\x12\x1a\n\rerror_message\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code\"\x89\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x14\n\x0chome_address\x18\x04 \x01(\t\x12\x0e\n\x06gender\x18\x05 \x01(\t\x12\x18\n\x0bis_featured\x18\x06 \x01(\x08H\x00\x88\x01\x01\x42\x0e\n\x0c_is_featured\"\xe7\x01\n\x0cUserResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x14\n\x0chome_address\x18\x04 \x01(\t\x12\x0e\n\x06gender\x18\x05 \x01(\t\x12\x18\n\x0bis_featured\x18\x06 \x01(\x08H\x00\x88\x01\x01\x12\x1a\n\rerror_message\x18\x07 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nerror_code\x18\x08 \x01(\x05H\x02\x88\x01\x01\x42\x0e\n\x0c_is_featuredB\x10\n\x0e_error_messageB\r\n\x0b_error_code\"\x14\n\x06UserId\x12\n\n\x02id\x18\x01 \x01(\t2\xbc\x01\n\x0bUserService\x12*\n\x08Register\x12\n.user.User\x1a\x12.user.EmptyMessage\x12+\n\x07GetById\x12\x0c.user.UserId\x1a\x12.user.UserResponse\x12(\n\x06Update\x12\n.user.User\x1a\x12.user.EmptyMessage\x12*\n\x06\x44\x65lete\x12\x0c.user.UserId\x1a\x12.user.EmptyMessageb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTYMESSAGE._serialized_start=20
  _EMPTYMESSAGE._serialized_end=120
  _USER._serialized_start=123
  _USER._serialized_end=260
  _USERRESPONSE._serialized_start=263
  _USERRESPONSE._serialized_end=494
  _USERID._serialized_start=496
  _USERID._serialized_end=516
  _USERSERVICE._serialized_start=519
  _USERSERVICE._serialized_end=707
# @@protoc_insertion_point(module_scope)
