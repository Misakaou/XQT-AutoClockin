from csv import reader
from io import StringIO
from os import environ, getcwd
import os
from random import shuffle
from utils.Config import Config

class UserReader:
    _csv_file = None
    _id_header_list = None
    _id_list_dict_content = None
    _env_config = None
    
    def __init__(self) -> None:
        self._env_config = environ.get('ACTION_ENABLED', 'false') == 'true'
        if self._env_config:
            self._csv_file = StringIO(os.environ.get('CLOCKIN_USERS', ''))
            csv_reader = reader(self._csv_file)
        else:
            self._csv_file = open(getcwd() + '/' +  Config().get_config_str('idlist', 'file_name'), 'r', encoding='utf-8')
            csv_reader = reader(self._csv_file)
        self._id_header_list = next(csv_reader)
        self._id_list_dict_content = [dict(zip(self._id_header_list, row)) for row in csv_reader]
    
    def get_user_dict_list(self) -> list:
        if len(self._id_list_dict_content) > 1:
            shuffle(self._id_list_dict_content)
        return self._id_list_dict_content


if __name__=='__main__': # test
    idreader = UserReader()
    print(idreader.get_user_dict_list())
