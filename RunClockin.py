import logging
from Clockin import *
from utils.UserReader import UserReader

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)

class RunClockin:
    _user_list = None
    
    def __init__(self) -> None:
        logging.info(Language().get_message('name') + '-' + Config().get_config_str('app', 'name'))
        logging.info(Language().get_message('author') + '-' + Config().get_config_str('app', 'author'))
        logging.info(Language().get_message('version') + '-' + Config().get_config_str('app', 'version'))
        self._user_list = UserReader().get_user_list()
        if len(self._user_list) > 1:
            self._user_list = shuffle(self._user_list)
        
    def run_multi_thread(self) -> None:
        # TODO
        pass
        
    def run(self) -> None:
        for user in self._user_list:
            ShixiClockin(user).clockin()
            logging.info(Language().get_message('split_line'))
            ClockinOrdinary(user).clockin()
            logging.info(Language().get_message('split_line'))
            sleep(randint(1, 3))

if __name__ == '__main__':
    run_clockin = RunClockin()
    run_clockin.run()
