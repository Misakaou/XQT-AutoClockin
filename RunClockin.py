import io
from os import environ
from time import sleep
from random import uniform

from utils.Email import Email
from utils.UserReader import UserReader
from utils.Log import Log
from utils.Language import Language
from utils.Config import Config
from Clockin import ClockinShixi, ClockinOrdinary

LANGUAGE = Language()
CONFIG = Config()


class RunClockin:
    _user_list = None
    _github_action = False
    _log = Log('RUNNER')
    
    def __init__(self) -> None:
        self._log.get_logger().info(LANGUAGE.get_message('name') + '-' + CONFIG.get_config_str('app', 'name'))
        self._log.get_logger().info(LANGUAGE.get_message('author') + '-' + CONFIG.get_config_str('app', 'author'))
        self._log.get_logger().info(LANGUAGE.get_message('version') + '-' + CONFIG.get_config_str('app', 'version'))
        self._github_action = CONFIG.get_is_env()
        if self._github_action == 'true' or self._github_action == 'debug':
            self._log.get_logger().info(LANGUAGE.get_message('github_action_enabled'))
        else:
            self._log.get_logger().info(LANGUAGE.get_message('github_action_disabled'))
        self._user_list = UserReader().get_user_dict_list()
    
    def run_multi_thread(self) -> None:
        # TODO
        pass
    
    def run_in_order(self) -> None:
        is_all_user_clokcin_success = False
        for user in self._user_list:
            current_user_log_string_io = io.StringIO()
            current_user_log_handler = self._log.add_stringio_handler(current_user_log_string_io)
            retry_count = CONFIG.get_config_int('app', 'retry_max_count')
            is_current_user_shixi_clockin_success = False
            is_current_user_ordinary_clockin_success = False
            
            while not is_current_user_shixi_clockin_success and retry_count > 0:
                is_current_user_shixi_clockin_success = ClockinShixi(self._log, user).clockin()
                retry_count -= 1
            self._log.get_logger().info(LANGUAGE.get_message('split_line'))
            
            retry_count = CONFIG.get_config_int('app', 'retry_max_count')
            while not is_current_user_ordinary_clockin_success and retry_count > 0:
                is_current_user_ordinary_clockin_success = ClockinOrdinary(self._log, user).clockin()
                retry_count -= 1
            self._log.get_logger().info(LANGUAGE.get_message('split_line'))
            
            is_all_user_clokcin_success &= is_current_user_shixi_clockin_success and is_current_user_ordinary_clockin_success
            self._log.remove_stringio_handler(current_user_log_handler)
            if is_current_user_shixi_clockin_success and is_current_user_ordinary_clockin_success:
                self._log.get_logger().info(LANGUAGE.get_message('email_send_to_user_cancel') + '-' + user.get('id') + '-' + user.get('remarks') + '-' + user.get('email'))
            else:
                if self.send_email_user(user, current_user_log_string_io.getvalue()):
                    self._log.get_logger().info(LANGUAGE.get_message('email_send_to_user_success') + '-' + user.get('id') + '-' + user.get('remarks') + '-' + user.get('email'))
                else:
                    self._log.get_logger().error(LANGUAGE.get_message('email_send_to_user_fail') + '-' + user.get('id') + '-' + user.get('remarks') + '-' + user.get('email'))
            self._log.get_logger().info(LANGUAGE.get_message('split_line'))
            sleep(round(uniform(0, CONFIG.get_config_float('clockinrunner', 'sleep_seconds_max')), 3))
        self.send_email_all()
    
    def send_email_user(self, user_json:dict, user_log: str) -> bool:
        if CONFIG.get_config_bool('email', 'enabled'):
            email = Email(CONFIG.get_config_str('email', 'smtp_host'), CONFIG.get_config_str('email', 'smtp_port'), CONFIG.get_config_str('email', 'smtp_address'), CONFIG.get_config_str('email', 'smtp_password'))
            return email.send([user_json.get('email')], LANGUAGE.get_message('email_title_user').format(userid=user_json.get('id')), user_log)
    
    def send_email_all(self) -> None:
        if CONFIG.get_config_bool('email', 'enabled'):
            email_text = ''
            email = Email(CONFIG.get_config_str('email', 'smtp_host'), CONFIG.get_config_str('email', 'smtp_port'), CONFIG.get_config_str('email', 'smtp_address'), CONFIG.get_config_str('email', 'smtp_password'))
            
            if environ.get('ACTION_ENABLED', 'false') == 'debug': # DEBUG
                open('debug-config.log', 'w').write(self._log.get_info() + '\n' + CONFIG.get_config_str('email', 'smtp_host') + '\n' +  CONFIG.get_config_str('email', 'smtp_port') + '\n' +  CONFIG.get_config_str('email', 'smtp_address') + '\n' +  CONFIG.get_config_str('email', 'smtp_password') + '\n' + str(CONFIG.get_config_list('email', 'smtp_receiver_list')) + '\n')
                open('debug-full.log', 'w').write(self._log.get_info())
            
            if CONFIG.get_config_str('email', 'send_log_level') == 'error':
                email_text = self._log.get_error()
            elif CONFIG.get_config_str('email', 'send_log_level') == 'warning':
                email_text = self._log.get_warning()
            elif CONFIG.get_config_str('email', 'send_log_level') == 'info':
                email_text = self._log.get_info()
            else:
                email_text = self._log.get_warning()
            
            if len(email_text):
                if email.send(CONFIG.get_config_list('email', 'smtp_receiver_list'), LANGUAGE.get_message('email_title'), email_text):
                    self._log.get_logger().info(LANGUAGE.get_message('email_send_success'))
                else:
                    self._log.get_logger().error(LANGUAGE.get_message('email_send_fail'))
            else:
                self._log.get_logger().info(LANGUAGE.get_message('email_send_cancel'))
            
            email.quit()
        else:
            self._log.get_logger().info(LANGUAGE.get_message('email_not_enabled'))

if __name__ == '__main__':
    RunClockin().run_in_order()
