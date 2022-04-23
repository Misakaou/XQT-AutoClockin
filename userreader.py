from csv import reader
from os import getcwd
from config import Config

class UserReader:
    __csv_file = None
    __id_header_list = None
    __id_list_dict_content = None
    
    def __init__(self) -> None:
        self.__csv_file = getcwd() + '/' +  Config().get_config_str('idlist', 'file_name')
        self.__id_header_list = Config().get_config_list('idlist', 'header')
        self.__id_list_dict_content = [dict(zip(self.__id_header_list, row)) for row in reader(open(self.__csv_file))][1:]
        
    def get_user_list(self) -> list:
        return self.__id_list_dict_content


if __name__=='__main__': # test
    idreader = UserReader()
    print(idreader.get_user_list())