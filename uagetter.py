from os import getcwd
from random import choice
from config import Config

class UAGetter:
    __ua_list_file_name = []
    def __init__(self):
        self.__ua_list_file_name = getcwd() + '/' + Config().get_config_str('useragent', 'ua_list_file_name')

    def get_random_ua(self):
        lines = open(self.__ua_list_file_name, 'r').readlines()
        return choice(lines)

if __name__ == '__main__': # test
    uagetter = UAGetter()
    print(uagetter.get_random_ua())
