from csv import reader
from os import getcwd
from random import shuffle
from Config import Config

class UserReader:
    _csv_file = None
    _id_header_list = None
    _id_list_dict_content = None
    
    def __init__(self) -> None:
        self._csv_file = getcwd() + '/' +  Config().get_config_str('idlist', 'file_name')
        with open(self._csv_file, 'r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file)
            self._id_header_list = next(csv_reader)
            self._id_list_dict_content = [dict(zip(self._id_header_list, row)) for row in csv_reader]
    
    def get_user_dict_list(self) -> list:
        if len(self._id_list_dict_content) > 1:
            shuffle(self._id_list_dict_content)
        return self._id_list_dict_content


if __name__=='__main__': # test
    idreader = UserReader()
    print(idreader.get_user_dict_list())
