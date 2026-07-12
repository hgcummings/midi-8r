SHIMMER_LOCATION = {'off': 0x10, 'hall': 0x14, 'plate': 0x18, 'spring': 0x1c}

MIDI_CC_REVERB = 37

SPRING = 0
PLATE = 1
HALL = 2
SHIMMER = 3

NAMES = ['Sprng','Plate','Hall','Shimr']

class Reverb:
    """
    Simple prop editor for setting the reverb model on the NUX Cerberus pedal
    Not a full component in itself. Needs to be wrapped in PresetEditor or DirectMenu
    """
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out

    def load(self, data):
        self.state = data[0]
        self.saved_state = self.state

    def save(self):
        if (self.state != self.saved_state):
            # The Cerberus has "slots" for three reverb types
            # By default these contain: Spring, Plate, Hall
            # The shimmer model can be placed in any one of these slots,
            # on a per-patch basis.
            # This is likely a flash write so we only do it as needed.
            if (self.state == SHIMMER):
                # Put the Shimmer model in the 'hall' slot
                # (making Hall unavailable to this preset)
                self.__set_shimmer_location('hall')
            else:
                self.__set_shimmer_location('off')

        # Set the reverb type cleanly now we know there's a slot containing it
        self.__set_reverb_type(self.state)
        self.saved_state = self.state
        return (self.state,)

    def value_range(self):
        return (0, self.state, 3)

    def update_value(self, value):
        self.state = value
        self.__set_reverb_type(self.state)

    def switch(self):
        pass
    
    def has_changed(self):
        return self.state != self.saved_state

    def render(self, display, colour=(255,255,255)):
        display.show_text(NAMES[self.state], colour=colour)

    def __set_reverb_type(self, id):
        self.midi_out.send_control_change(1, MIDI_CC_REVERB, id)

    def __set_shimmer_location(self, where):
        # Note: this immediately persists to the current preset,
        #       whether or not its currently in edit mode
        self.__send_sysex([0xF0,0x00,0x11,0x22,0x20,0x00,0x70,0x05,
            0x06,0x01,SHIMMER_LOCATION[where],0x00,0x00,0xF7])

    def __send_sysex(self, data):
        self.midi_out.send_raw_bytes(bytes(data))