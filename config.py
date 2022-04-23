from configparser import ConfigParser
import json
from os import getcwd
from typing import Any

class Config:
    __config = ConfigParser()
    
    def __init__(self) -> None:
        self.__config.read(getcwd() + '/config.conf')
    
    def get_config_str(self, section, field) -> str:
        return self.__config[section][field]
    
    def get_config_list(self, section, field) -> list:
        return list(self.__config[section][field].strip('][').split(', '))
    
    def get_config_json(self, section, field) -> dict:
        return json.loads(self.__config[section][field])
    
    def get_language(self) -> str:
        return self.__config['app']['language']
    
    def get_version(self) -> str:
        return self.__config['app']['version']


if __name__ == '__main__': # test
    config = Config()
    print(config.get_config_str('idlist', 'file_name'))
    print(config.get_config_json('clockinapi', 'shixi_qian_body'))
