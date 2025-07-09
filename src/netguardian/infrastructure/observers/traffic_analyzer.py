from collections import defaultdict
from src.netguardian.domain.packet import Packet

class TrafficAnalyzer:
    '''Observer that performs basic traffic analysis (e.g., volume per IP).'''
    def __init__(self):
        self.volume_by_source_ip = defaultdict(int)

    def update(self, packet: Packet) -> None:
        self.volume_by_source_ip[packet.source_ip] += packet.length
    
    def report(self) -> None:
        print('\n--- Traffic Analysis Report ---')
        if not self.volume_by_source_ip:
            print('No traffic captured.')
            return
            
        print('Total data sent per source IP:')
        sorted_ips = sorted(
            self.volume_by_source_ip.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        for ip, total_bytes in sorted_ips[:10]: # Top 10
            print(f'- {ip:<15}: {total_bytes / 1024:.2f} KB')
        print('-----------------------------\n')