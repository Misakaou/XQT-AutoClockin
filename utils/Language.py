from os import getcwd
import yaml
from utils.Config import Config

class Language:
    __lang = None
    __language_file = None
    __language_content = None
    
    def __init__(self) -> None:
        self.__lang = Config().get_language()
        self.__language_file = getcwd() + '/language/' + self.__lang + '.yml'
        with open(self.__language_file, 'r') as file:
            self.__language_content = yaml.safe_load(file)
        # if version
        if self.__language_content['version'] != Config().get_version():
            raise AttributeError('[lang] version inconsistency.')
            
    def get_message(self, message_name) -> str:
        return self.__language_content['message'][message_name]


if __name__ == '__main__': # test
    language = Language()
    print(language.get_message('name'))