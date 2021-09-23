import enums

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
        
