from configparser import ConfigParser
import json
from os import getcwd
from typing import Any

class Config:
    _config = ConfigParser()
    
    def __init__(self) -> None:
        self._config.read(getcwd() + '/config.conf')
        
    def get_config_bool(self, section, field) -> bool:
        print(self._config[section][field] == 'true')
        return self._config[section][field] == 'true'
    
    def get_config_float(self, section, field) -> float:
        return float(self._config[section][field])
    
    def get_config_int(self, section, field) -> int:
        return int(self._config[section][field])
    
    def get_config_str(self, section, field) -> str:
        return self._config[section][field]
    
    def get_config_list(self, section, field) -> list:
        return list(self._config[section][field].strip('][').split(','))
    
    def get_config_json(self, section, field) -> dict:
        return json.loads(self._config[section][field])
    
    def get_language(self) -> str:
        return self._config['app']['language']
    
    def get_version(self) -> str:
        return self._config['app']['version']


if __name__ == '__main__': # test
    config = Config()
    print(config.get_config_str('idlist', 'file_name'))
    print(config.get_config_json('clockinapi', 'shixi_qian_body'))
