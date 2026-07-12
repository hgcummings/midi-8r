import struct

def load_empty(param):
    """Load a parameter with zeroed data, returning the bytes for persistence."""
    empty = bytes(struct.calcsize(param.format))
    param.load(struct.unpack(param.format, empty))
    return empty
