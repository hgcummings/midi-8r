import os

class FileStorage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.presets = bytearray(128)        
        try:
            with open(self.file_path, "rb") as f:
                self.presets = bytearray(f.read())
        except OSError:
            with open(self.file_path, "wb") as f:
                f.write(self.presets)

    def get_preset(self, patch):
        return self.presets[patch]

    def set_preset(self, patch, preset):
        self.presets[patch] = preset
        with open(self.file_path, "wb") as f:
            f.write(self.presets)