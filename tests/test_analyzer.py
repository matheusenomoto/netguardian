from datetime import datetime
from src.netguardian.domain.packet import Packet
from src.netguardian.infrastructure.observers.traffic_analyzer import TrafficAnalyzer

def test_traffic_analyzer_volume_calculation():
    # Arrange
    analyzer = TrafficAnalyzer()
    p1 = Packet(datetime.now(), '192.168.1.1', '8.8.8.8', 'UDP', 100, '')
    p2 = Packet(datetime.now(), '192.168.1.2', '8.8.8.8', 'TCP', 250, '')
    p3 = Packet(datetime.now(), '192.168.1.1', '8.8.4.4', 'UDP', 150, '')

    # Act
    analyzer.update(p1)
    analyzer.update(p2)
    analyzer.update(p3)

    # Assert
    assert analyzer.volume_by_source_ip['192.168.1.1'] == 250  # 100 + 150
    assert analyzer.volume_by_source_ip['192.168.1.2'] == 250
    assert '10.0.0.1' not in analyzer.volume_by_source_ip