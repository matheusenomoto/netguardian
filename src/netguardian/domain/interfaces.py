from abc import ABC, abstractmethod
from typing import Protocol
from .packet import Packet

class PacketObserver(Protocol):
    '''
    Defines the interface for any class that wants to be notified of new packets.
    Using a Protocol for structural typing
    '''
    def update(self, packet: Packet) -> None:
        ...
    
class PacketCapture(ABC):
    '''
    Abstract interface for a packet capture source.
    This allows us to swap Scapy for another tool without changing the application logic.
    '''
    @abstractmethod
    def start(self, on_packet_callback) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
