from .midi_message_types import *

class MidiStreamReader:
    def __init__(self, channel, message_handler):
        self.channel = channel
        self.handler = message_handler
        self.buffer = memoryview(bytearray(3))
        self.msg_length = 0
        
    def write(self, next_bytes):
        for next_byte in next_bytes:
            if next_byte > 127: # Status byte; start of a new message
                if (self.msg_length > 0): # A message in the buffer we haven't handled yet
                    self.handler.on_unknown_message(self.buffer[:self.msg_length])
                self.buffer[0] = next_byte
                self.msg_length = 1
            else: # Data byte; part of an already-started message
                if self.msg_length == len(self.buffer):
                    # Already filled the buffer without recognising the message
                    self.handler.on_unknown_message(self.buffer)
                    self.buffer[0] = next_byte
                    self.msg_length = 1
                else:
                    self.buffer[self.msg_length] = next_byte
                    self.msg_length += 1
        
            # Check if we have a complete message we want to handle
            if self.buffer[0] & 15 == self.channel: # (Ignore anything not on our channel)
                if self.msg_length == 2 and (self.buffer[0] >> 4) == PROGRAM_CHANGE:
                    self.handler.on_program_change(self.buffer[1])
                    self.msg_length = 0
                elif self.msg_length == 3 and (self.buffer[0] >> 4) == CONTROL_CHANGE:
                    self.handler.on_control_change(self.buffer[1], self.buffer[2])
                    self.msg_length = 0
