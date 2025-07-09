from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Packet:
    '''
    Represents a single network packet
    This is a core domain entity. It is imutable.
    '''
    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    length: int
    payload_summary: str
