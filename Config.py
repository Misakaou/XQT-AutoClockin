from configparser import ConfigParser
import json
from os import getcwd, environ

class Config:
    _config = ConfigParser()
    _env_config = None
    
    def __init__(self) -> None:
        self._config.read(getcwd() + '/config.conf')
        self._env_config = environ.get('ACTION_ENABLED', 'false')
        
    def get_config_bool(self, section:str, field:str) -> bool:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = environ.get((section + '_' + field).upper(), 'false') == 'true'
            if ret: return ret
        return self._config[section][field] == 'true'
    
    def get_config_float(self, section:str, field:str) -> float:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = float(environ.get((section + '_' + field).upper(), '0.0'))
            if ret: return ret
        return float(self._config[section][field])
    
    def get_config_int(self, section:str, field:str) -> int:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = int(environ.get((section + '_' + field).upper(), '0'))
            if ret: return ret
        return int(self._config[section][field])
    
    def get_config_str(self, section:str, field:str) -> str:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = environ.get((section + '_' + field).upper(), '')
            if ret: return ret
        return self._config[section][field]
    
    def get_config_list(self, section:str, field:str) -> list:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = environ.get((section + '_' + field).upper(), '').split(',')
            if ret: return ret
        return list(self._config[section][field].strip('][').split(','))
    
    def get_config_json(self, section:str, field:str) -> dict:
        if self._env_config == 'true' or self._env_config == 'debug':
            ret = json.loads(environ.get((section + '_' + field).upper(), '{}'))
            if ret: return ret
        return json.loads(self._config[section][field])
    
    def get_is_env(self) -> str:
        return self._env_config
    
    def get_language(self) -> str:
        if self._env_config:
            return environ.get('app_language'.upper(), 'zh_cn')
        else:
            return self._config['app']['language']
    
    def get_version(self) -> str:
        return self._config['app']['version']


if __name__ == '__main__': # test
    config = Config()
    print(config.get_config_str('idlist', 'file_name'))
    print(config.get_config_json('clockinapi', 'shixi_qian_body'))
