from src.netguardian.domain.interfaces import PacketCapture
from src.netguardian.common.observable import Observable
from src.netguardian.domain.packet import Packet

class MonitorTrafficUseCase:
    '''
    This use case orchestrates the process of monitoring network traffic.
    It depends on abstractions (interfaces), not concrete implementations.
    '''
    def __init__(self, packet_capture: PacketCapture, observable: Observable):
        self._packet_capture = packet_capture
        self._observable = observable

    def _handle_packet(self, packet: Packet) -> None:
        '''Callback function to be executed for each captured packet.'''
        self._observable.notify(packet)

    def execute(self) -> None:
        '''Starts the traffic monitoring process.'''
        try:
            self._packet_capture.start(on_packet_callback=self._handle_packet)
        finally:
            self._packet_capture.stop()