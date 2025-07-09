from src.netguardian.domain.packet import Packet

class ConsolePresenter:
    '''
    Observer that formats and prints packet data to the console.
    '''
    def update(self, packet: Packet) -> None:
        ts = packet.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        print(
            f'[{ts}] {packet.protocol:<5} | '
            f'{packet.source_ip:<15} -> {packet.destination_ip:<15} | '
            f'{packet.length:<5} bytes | {packet.payload_summary}'
        )