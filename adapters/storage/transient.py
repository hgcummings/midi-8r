class TransientStorage:
    def __init__(self):
        self.presets = [0 for _ in range(128)]

    def get_preset(self, patch):
        return self.presets[patch]

    def set_preset(self, patch, preset):
        self.presets[patch] = preset