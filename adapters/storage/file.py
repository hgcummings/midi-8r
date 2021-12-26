import mmap

class FileStorage:
    def __init__(self, fileno):
        self.mm = mmap.mmap(fileno, 128, access=mmap.ACCESS_WRITE)

    def get_preset(self, patch):
        return self.mm[patch]

    def set_preset(self, patch, preset):
        self.mm[patch] = preset
        self.mm.flush()