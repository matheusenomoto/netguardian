import configparser
from typing import Optional

def load_config(path: str = 'config.ini') -> dict:
    '''
    Loads configuration from an INI file.
    '''
    config = configparser.ConfigParser()
    config.read(path)
    return {
        'interface': config.get('monitoring', 'interface', fallback=None) or None,
        'enable_file_logging': config.getboolean('logging', 'enable_file_logging'),
        'log_file': config.get('logging', 'log_file', fallback='traffic.csv'),
    } 