import sys
import os

# Add src to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from netguardian.application.use_cases import MonitorTrafficUseCase
from netguardian.infrastructure.capture.scapy_capture import ScapyPacketCapture
from netguardian.infrastructure.observers.console_presenter import ConsolePresenter
from netguardian.infrastructure.observers.file_logger import FileLogger
from netguardian.infrastructure.observers.traffic_analyzer import TrafficAnalyzer
from netguardian.infrastructure.config.loader import load_config
from netguardian.common.observable import Observable

def main():
    '''
    The Composition Root.
    This is where we instantiate concrete classes and 'wire' them together.
    '''
    try:
        # 1. Load Configuration
        config = load_config()

        # 2. Instantiate Infrastructure Components
        packet_capture_source = ScapyPacketCapture(interface=config['interface'])
        
        # 3. Instantiate Observers (our event listeners)
        console_presenter = ConsolePresenter()
        traffic_analyzer = TrafficAnalyzer()
        
        # 4. Set up the Observable (the event source)
        observable = Observable()
        observable.register(console_presenter)
        observable.register(traffic_analyzer)

        file_logger = None
        if config['enable_file_logging']:
            file_logger = FileLogger(config['log_file'])
            observable.register(file_logger)

        # 5. Instantiate the Use Case, injecting dependencies
        monitor_use_case = MonitorTrafficUseCase(packet_capture_source, observable)

        # 6. Execute the Use Case
        monitor_use_case.execute()

    except PermissionError:
        print('\n[ERROR] Permission denied. Please run this script with root privileges (e.g., \'sudo python main.py\').')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nMonitoring stopped by user.')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
    finally:
        # 7. Clean up resources
        if 'traffic_analyzer' in locals():
            traffic_analyzer.report()
        if 'file_logger' in locals() and file_logger:
            file_logger.close()
            print('File logger closed.')
        print('NetGuardian has shut down gracefully.')


if __name__ == '__main__':
    main()