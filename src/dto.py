import enums
from json import dumps, loads
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

#marshmallow API reference: https://marshmallow.readthedocs.io/en/stable/index.html

# DTO current proposed structure on version 1.
#{
#   "harena-log-stream-version": 1
#   "harena-log-stream": [
#       "topic": "topic_name",
#       "payload": "any content here"
#   ]
#}
#

class ArenaLoggerDtoValidator():
    @staticmethod
    def validateDto(message):
        if 'harena-log-stream-version' not in message :
              message['harena-log-stream-version'] = str(enums.StreamVersionSpecialCodes.NOT_IDENTIFIED.value)
        
        #TODO: create an exception handler with custom exceptions
       
        if 'harena-log-stream' not in message:
            raise ValueError('Message does not contains harena-log-stream')
        
        for harena_stream_log_value in message['harena-log-stream']:
            if 'topic' not in harena_stream_log_value:
                raise ValueError('One or more harena-log-stream items does not contains topic')
                break
            
            if 'payload' not in harena_stream_log_value:
                raise ValueError("One or more harena-log-stream items does not contains payload")
                break

            if not bool(harena_stream_log_value['payload']):
                raise ValueError("One or more harena-log-stream items does not contains key-value pair")

 #TODO: create a validator using marshmallow api for dto.
class HarenaLogergStream(Schema):
    topic = fields.String()
    payload = fields.Dict()
        
class LoggerDto(Schema):
    harena_log_stream_version = fields.Int(required=True, data_key="harena-log-stream-version")
    harena_log_stream = fields.Nested(HarenaLogergStream(many=True), data_key="harena-log-stream")
    server_timestamp = fields.String()

