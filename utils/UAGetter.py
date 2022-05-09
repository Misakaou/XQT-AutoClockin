from os import getcwd
from random import choice
from utils.Config import Config

class UAGetter:
    __ua_list_file_name = []
    def __init__(self):
        self.__ua_list_file_name = getcwd() + '/utils/' + Config().get_config_str('useragent', 'ua_list_file_name')

    def get_random_ua(self) -> str:
        lines = open(self.__ua_list_file_name, 'r').readlines()
        return str(choice(lines)).strip('\n')

if __name__ == '__main__': # test
    uagetter = UAGetter()
    print(uagetter.get_random_ua())
