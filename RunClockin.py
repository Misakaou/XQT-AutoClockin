import os
from time import sleep
from random import uniform
from Clockin import *
from utils.Email import Email
from utils.UserReader import UserReader
from utils.Log import *

class RunClockin:
    _user_list = None
    _github_action = False
    
    def __init__(self) -> None:
        logger.info(LANGUAGE.get_message('name') + '-' + CONFIG.get_config_str('app', 'name'))
        logger.info(LANGUAGE.get_message('author') + '-' + CONFIG.get_config_str('app', 'author'))
        logger.info(LANGUAGE.get_message('version') + '-' + CONFIG.get_config_str('app', 'version'))
        if os.environ.get('ACTION_ENABLED', 'false') == 'true':
            logger.info(LANGUAGE.get_message('ACTION_ENABLED'))
            self._github_action = True
        else:
            logger.info(LANGUAGE.get_message('github_action_disabled'))
        self._user_list = UserReader(self._github_action).get_user_dict_list()
    
    def run_multi_thread(self) -> None:
        # TODO
        pass
    
    def run_in_order(self) -> None:
        for user in self._user_list:
            ClockinShixi(user).clockin()
            logger.info(LANGUAGE.get_message('split_line'))
            ClockinOrdinary(user).clockin()
            logger.info(LANGUAGE.get_message('split_line'))
            sleep(round(uniform(0, CONFIG.get_config_float('clockinrunner', 'sleep_seconds_max')), 3))
        if CONFIG.get_config_bool('email', 'enabled') or os.environ.get('EMAIL_ENABLED', 'false') == 'true':
            email_text = ''
            email = None
            if self._github_action:
                email = Email(os.environ.get('EMAIL_SMTP_HOST', ''), os.environ.get('EMAIL_SMTP_PORT', ''), os.environ.get('EMAIL_SMTP_ADDRESS', ''), os.environ.get('EMAIL_SMTP_PASSWORD', ''))
                if os.environ.get('EMAIL_SEND_LOG_LEVEL', '') == 'error':
                    email_text = log_stream_error.getvalue()
                elif os.environ.get('EMAIL_SEND_LOG_LEVEL', '') == 'info':
                    email_text = log_stream_info.getvalue()
                elif os.environ.get('EMAIL_SEND_LOG_LEVEL', '') == 'warning':
                    email_text = log_stream_warning.getvalue()
                else:
                    email_text = log_stream_warning.getvalue()
            else:
                email = Email(CONFIG.get_config_str('email', 'smtp_host'), CONFIG.get_config_str('email', 'smtp_port'), CONFIG.get_config_str('email', 'smtp_address'), CONFIG.get_config_str('email', 'smtp_password'))
                if CONFIG.get_config_str('email', 'send_log_level') == 'error':
                    email_text = log_stream_error.getvalue()
                elif CONFIG.get_config_str('email', 'send_log_level') == 'warning':
                    email_text = log_stream_warning.getvalue()
                elif CONFIG.get_config_str('email', 'send_log_level') == 'info':
                    email_text = log_stream_info.getvalue()
                else:
                    email_text = log_stream_warning.getvalue()
            
            if len(email_text):
                if email.send(CONFIG.get_config_list('email', 'email_receiver'), LANGUAGE.get_message('email_title'), email_text):
                    logger.info(LANGUAGE.get_message('email_send_success'))
                else:
                    logger.error(LANGUAGE.get_message('email_send_fail'))
            else:
                logger.info(LANGUAGE.get_message('email_send_cancel'))
            
            email.quit()
        else:
            logger.info(LANGUAGE.get_message('email_not_enabled'))

if __name__ == '__main__':
    RunClockin().run_in_order()
