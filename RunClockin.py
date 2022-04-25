from Clockin import *
from utils.Email import Email
from utils.UserReader import UserReader
from utils.Log import *

class RunClockin:
    _user_list = None
    
    def __init__(self) -> None:
        logger.info(Language().get_message('name') + '-' + Config().get_config_str('app', 'name'))
        logger.info(Language().get_message('author') + '-' + Config().get_config_str('app', 'author'))
        logger.info(Language().get_message('version') + '-' + Config().get_config_str('app', 'version'))
        self._user_list = UserReader().get_user_list()
        if len(self._user_list) > 1:
            self._user_list = shuffle(self._user_list)
        
    def run_multi_thread(self) -> None:
        # TODO
        pass
        
    def run(self) -> None:
        for user in self._user_list:
            ShixiClockin(user).clockin()
            logger.info(Language().get_message('split_line'))
            ClockinOrdinary(user).clockin()
            logger.info(Language().get_message('split_line'))
            sleep(randint(1, 3))
        if Config().get_config_bool('email', 'enabled'):
            email_text = ''
            email = Email(Config().get_config_str('email', 'smtp_host'), Config().get_config_str('email', 'smtp_port'), Config().get_config_str('email', 'smtp_address'), Config().get_config_str('email', 'smtp_password'))
            if Config().get_config_str('email', 'send_log_level') == 'error':
                email_text = log_stream_error.getvalue()
            else:
                email_text = log_stream_warning.getvalue()
            if len(email_text):
                if email.send(Config().get_config_list('email', 'email_receiver'), Language().get_message('email_title'), email_text):
                    logger.info(Language().get_message('email_send_success'))
                else:
                    logger.error(Language().get_message('email_send_fail'))
            else:
                logger.info(Language().get_message('email_send_cancel'))
            email.quit()

if __name__ == '__main__':
    run_clockin = RunClockin()
    run_clockin.run()
