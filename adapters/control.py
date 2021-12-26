from enum import Enum, auto

class EncoderEvent(Enum):
    INCREMENT = auto(),
    DECREMENT = auto(),
    PUSH = auto(),
    RELEASE = auto()