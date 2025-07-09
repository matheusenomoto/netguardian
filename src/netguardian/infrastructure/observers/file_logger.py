import csv
from src.netguardian.domain.packet import Packet

class FileLogger:
    '''
    Observer that logs packet data to a CSV file.
    '''
    def __init__(self, filename: str):
        self._filename = filename
        self._file_handler = open(self._filename, 'w', newline='')
        self._writer = csv.writer(self._file_handler)
        # Write header
        self._writer.writerow([
            'timestamp', 'source_ip', 'destination_ip', 
            'protocol', 'length', 'payload_summary'
        ])
        print(f'FileLogger initialized. Logging to {self._filename}')

    def update(self, packet: Packet) -> None:
        self._writer.writerow([
            packet.timestamp.isoformat(),
            packet.source_ip,
            packet.destination_ip,
            packet.protocol,
            packet.length,
            packet.payload_summary
        ])

    def close(self) -> None:
        self._file_handler.close()