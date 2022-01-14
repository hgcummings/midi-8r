from .midi_message_types import *

class MidiStreamReader:
    def __init__(self, message_handler):
        self.handler = message_handler
        self.buffer = memoryview(bytearray(3))
        self.msg_length = 0
        
    def consume(self, next_bytes):
        '''
        Consume bytes from the underlying stream.

        The important invariant here is that each byte must be handled exactly once
        (even for unrecognised message types). This allows the handler to correctly
        implement MIDI pass-through functionality if needed.
        '''
        for next_byte in next_bytes:
            if self.msg_length == len(self.buffer) or (next_byte > 127 and self.msg_length > 0):
                # We've filled the buffer without recognising a message, or we're being given a
                # status byte (start of new message) while the current message is unrecognised.
                # So handle the current buffer contents as an unknown message, then reset.
                self.handler.on_unknown_message(self.buffer[:self.msg_length])
                self.msg_length = 0

            self.buffer[self.msg_length] = next_byte
            self.msg_length += 1
        
            # Check if we have a complete message that we can handle
            if self.msg_length == 2 and (self.buffer[0] >> 4) == PROGRAM_CHANGE:
                self.handler.on_program_change(self.buffer[0] & 15, self.buffer[1])
                self.msg_length = 0
            elif self.msg_length == 3 and (self.buffer[0] >> 4) == CONTROL_CHANGE:
                self.handler.on_control_change(self.buffer[0] & 15, self.buffer[1], self.buffer[2])
                self.msg_length = 0
