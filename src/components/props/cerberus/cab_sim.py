MIDI_CHANNEL = 0
MIDI_CC = 71

MODELS = [
    { 'layout': "1x12", 'character': "Jazz", 'indent_1': 0, 'indent_2': 2 },
    { 'layout': "1x12", 'character': "Warm", 'indent_1': 0, 'indent_2': 3 },
    { 'layout': "4x10", 'character': "Bass", 'indent_1': 0, 'indent_2': 0 },
    { 'layout': "2x12", 'character': "AC30", 'indent_1': 0, 'indent_2': 1 },
    { 'layout': "2x12", 'character': "Twin", 'indent_1': 0, 'indent_2': 2 },
    { 'layout': "4x12", 'character': "1960", 'indent_1': 0, 'indent_2': 0 },
    { 'layout': "4x12", 'character': "GrnBk", 'indent_1': 0, 'indent_2': 0 },
    { 'layout': "4x12", 'character': "Metal", 'indent_1': 0, 'indent_2': 1 },
]

class CabSim:
    """
    Component for selecting the cab sim (IR curve) on the NUX Cerberus
    """
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out
        self.alert = False

    def load(self, data):
        self.state = data[0]
        self.saved_state = self.state
        
        self.__update_midi()

    def save(self):
        self.saved_state = self.state
        return (self.state,)

    def show_view(self, display):
        self.__show_text(display)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.state, len(MODELS) - 1)

    def update_value(self, value, display):
        self.state = value
        self.__update_midi()
        self.__show_edit(display)

    def switch(self, display):
        return None

    def next(self):
        return None
    
    def __show_edit(self, display):
        self.__show_text(display, (32,255,32) if self.state == self.saved_state else (127,0,0))
    
    def __show_text(self, display, colour=(255,255,255)):
        model = MODELS[self.state]
        display.show_text(model['layout'], line2_text=model['character'],
            colour=colour,
            indent=model['indent_1'],
            line2_indent=model['indent_2'])

    def __update_midi(self):
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC, self.state)