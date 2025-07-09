from scapy.all import sniff, IP, TCP, UDP, DNS
from datetime import datetime
from typing import Callable
from src.netguardian.domain.packet import Packet
from src.netguardian.domain.interfaces import PacketCapture

class ScapyPacketCapture(PacketCapture):
    '''
    Concrete implementation of PacketCapture using the Scapy library.
    '''
    def __init__(self, interface: str | None = None):
        self._interface = interface
        self._stop_sniffing = False
        print(f'ScapyCapture configured for interface: {'default' if not interface else interface}')
    
    def _process_packet(self, scapy_pkt):
        if self._on_packet_callback and IP in scapy_pkt:
            protocol_map = {6: 'TCP', 17: 'UDP'}
            proto_name = protocol_map.get(scapy_pkt[IP].proto, 'Other')
            
            payload_summary = ""
            if scapy_pkt.haslayer(DNS) and scapy_pkt[DNS].qr == 0: # DNS Query
                payload_summary = f"DNS Query: {scapy_pkt[DNS].qd.qname.decode()}"
            elif scapy_pkt.haslayer(TCP):
                payload_summary = f"Ports: {scapy_pkt[TCP].sport}->{scapy_pkt[TCP].dport}"
            elif scapy_pkt.haslayer(UDP):
                 payload_summary = f"Ports: {scapy_pkt[UDP].sport}->{scapy_pkt[UDP].dport}"


            packet = Packet(
                timestamp=datetime.fromtimestamp(float(scapy_pkt.time)),
                source_ip=scapy_pkt[IP].src,
                destination_ip=scapy_pkt[IP].dst,
                protocol=proto_name,
                length=len(scapy_pkt),
                payload_summary=payload_summary
            )
            self._on_packet_callback(packet)
            
    def start(self, on_packet_callback: Callable[[Packet], None]) -> None:
        self._on_packet_callback = on_packet_callback
        self._stop_sniffing = False
        print("Starting packet capture... Press Ctrl+C to stop.")
        sniff(
            prn=self._process_packet, 
            iface=self._interface,
            store=False,
            stop_filter=lambda p: self._stop_sniffing
        )
        print("Packet capture stopped.")

    def stop(self) -> None:
        self._stop_sniffing = True