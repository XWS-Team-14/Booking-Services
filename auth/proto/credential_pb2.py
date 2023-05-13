# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: credential.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x63redential.proto\"]\n\x05\x45mpty\x12\x1a\n\rerror_message\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code\"\x81\x01\n\x0e\x41\x63tiveResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x1a\n\rerror_message\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x04 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code\"\x87\x01\n\x10ValidateResponse\x12\x11\n\tvalidated\x18\x01 \x01(\x08\x12\n\n\x02id\x18\x02 \x01(\t\x12\x1a\n\rerror_message\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x17\n\nerror_code\x18\x04 \x01(\x05H\x01\x88\x01\x01\x42\x10\n\x0e_error_messageB\r\n\x0b_error_code\"u\n\nCredential\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x11\n\x04role\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06\x61\x63tive\x18\x05 \x01(\x08H\x01\x88\x01\x01\x42\x07\n\x05_roleB\t\n\x07_active\"L\n\x11\x43heckedCredential\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x16\n\x0epassword_check\x18\x03 \x01(\t\"\xc1\x01\n\x12\x43redentialResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x11\n\x04role\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06\x61\x63tive\x18\x04 \x01(\x08H\x01\x88\x01\x01\x12\x1a\n\rerror_message\x18\x05 \x01(\tH\x02\x88\x01\x01\x12\x17\n\nerror_code\x18\x06 \x01(\x05H\x03\x88\x01\x01\x42\x07\n\x05_roleB\t\n\x07_activeB\x10\n\x0e_error_messageB\r\n\x0b_error_code\"?\n\x0b\x45mailUpdate\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\told_email\x18\x02 \x01(\t\x12\x11\n\tnew_email\x18\x03 \x01(\t\"H\n\x0ePasswordUpdate\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0cold_password\x18\x02 \x01(\t\x12\x14\n\x0cnew_password\x18\x03 \x01(\t\"\x1a\n\x0c\x43redentialId\x12\n\n\x02id\x18\x01 \x01(\t\" \n\x0f\x43redentialEmail\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"\xa1\x01\n\x05Token\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x1a\n\rrefresh_token\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x1a\n\rerror_message\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nerror_code\x18\x04 \x01(\x05H\x02\x88\x01\x01\x42\x10\n\x0e_refresh_tokenB\x10\n\x0e_error_messageB\r\n\x0b_error_code\"<\n\x0cTokenRefresh\x12\x1a\n\rrefresh_token\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x10\n\x0e_refresh_token2\xeb\x03\n\x11\x43redentialService\x12\x1f\n\x08Register\x12\x0b.Credential\x1a\x06.Empty\x12\x1c\n\x05Login\x12\x0b.Credential\x1a\x06.Token\x12-\n\x07GetById\x12\r.CredentialId\x1a\x13.CredentialResponse\x12\x33\n\nGetByEmail\x12\x10.CredentialEmail\x1a\x13.CredentialResponse\x12$\n\tGetActive\x12\x06.Token\x1a\x0f.ActiveResponse\x12#\n\x0bUpdateEmail\x12\x0c.EmailUpdate\x1a\x06.Empty\x12)\n\x0eUpdatePassword\x12\x0f.PasswordUpdate\x1a\x06.Empty\x12\x1c\n\nDeactivate\x12\x06.Token\x1a\x06.Empty\x12\x1f\n\x06\x44\x65lete\x12\r.CredentialId\x1a\x06.Empty\x12*\n\rValidateToken\x12\x06.Token\x1a\x11.ValidateResponse\x12%\n\x0cRefreshToken\x12\r.TokenRefresh\x1a\x06.Token\x12+\n\x0e\x43heckAuthority\x12\x06.Token\x1a\x11.ValidateResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'credential_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=20
  _EMPTY._serialized_end=113
  _ACTIVERESPONSE._serialized_start=116
  _ACTIVERESPONSE._serialized_end=245
  _VALIDATERESPONSE._serialized_start=248
  _VALIDATERESPONSE._serialized_end=383
  _CREDENTIAL._serialized_start=385
  _CREDENTIAL._serialized_end=502
  _CHECKEDCREDENTIAL._serialized_start=504
  _CHECKEDCREDENTIAL._serialized_end=580
  _CREDENTIALRESPONSE._serialized_start=583
  _CREDENTIALRESPONSE._serialized_end=776
  _EMAILUPDATE._serialized_start=778
  _EMAILUPDATE._serialized_end=841
  _PASSWORDUPDATE._serialized_start=843
  _PASSWORDUPDATE._serialized_end=915
  _CREDENTIALID._serialized_start=917
  _CREDENTIALID._serialized_end=943
  _CREDENTIALEMAIL._serialized_start=945
  _CREDENTIALEMAIL._serialized_end=977
  _TOKEN._serialized_start=980
  _TOKEN._serialized_end=1141
  _TOKENREFRESH._serialized_start=1143
  _TOKENREFRESH._serialized_end=1203
  _CREDENTIALSERVICE._serialized_start=1206
  _CREDENTIALSERVICE._serialized_end=1697
# @@protoc_insertion_point(module_scope)