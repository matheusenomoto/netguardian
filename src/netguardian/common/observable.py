from typing import List
from src.netguardian.domain.interfaces import PacketObserver
from src.netguardian.domain.packet import Packet

class Observable:
    '''
    Reusable implementation of the Observer pattern's subject.
    '''
    def __init__(self):
        self._observers: List[PacketObserver] = []

    def register(self, observer: PacketObserver) -> None:
        self._observers.append(observer)
    
    def unregister(self, observer: PacketObserver) -> None:
        self._observer.remove(observer)
    
    def notify(self, packet: Packet) -> None:
        for observer in self._observers:
            observer.update(packet)