class MidiMessageHandler:
    def on_program_change(self, channel, patch):
        '''
        Handle an incoming program change message
        '''
        pass
        
    def on_control_change(self, channel, number, value):
        '''
        Handle an incoming control change message
        '''
        pass

    def on_unknown_message(self, raw_bytes):
        '''
        Handle the raw bytes of an unrecognised message. Note that this might not be
        a complete message (long SysEx messages will be split across multiple calls)
        '''
        pass