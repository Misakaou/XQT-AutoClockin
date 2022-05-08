import io
from os import environ
from time import sleep
from random import uniform

from utils.Email import Email
from utils.UserReader import UserReader
from utils.Log import Log
from utils.Language import Language
from Config import Config
from Clockin import ClockinShixi, ClockinOrdinary

LANGUAGE = Language()
CONFIG = Config()
LOG = Log('RUNNER')

class RunClockin:
    _user_list = None
    _github_action = False
    
    def __init__(self) -> None:
        LOG.get_logger().info(LANGUAGE.get_message('name') + '-' + CONFIG.get_config_str('app', 'name'))
        LOG.get_logger().info(LANGUAGE.get_message('author') + '-' + CONFIG.get_config_str('app', 'author'))
        LOG.get_logger().info(LANGUAGE.get_message('version') + '-' + CONFIG.get_config_str('app', 'version'))
        self._github_action = CONFIG.get_is_env()
        if self._github_action == 'true' or self._github_action == 'debug':
            LOG.get_logger().info(LANGUAGE.get_message('github_action_enabled'))
        else:
            LOG.get_logger().info(LANGUAGE.get_message('github_action_disabled'))
        self._user_list = UserReader().get_user_dict_list()
    
    def run_multi_thread(self) -> None:
        # TODO
        pass
    
    def run_in_order(self) -> None:
        is_all_user_clokcin_success = False
        for user in self._user_list:
            current_user_log_string_io = io.StringIO()
            current_user_log_handler = LOG.add_stringio_handler(current_user_log_string_io)
            retry_count = CONFIG.get_config_int('app', 'retry_max_count')
            is_current_user_shixi_clockin_success = False
            is_current_user_ordinary_clockin_success = False
            
            while not is_current_user_shixi_clockin_success and retry_count > 0:
                is_current_user_shixi_clockin_success = ClockinShixi(LOG, user).clockin()
                retry_count -= 1
            LOG.get_logger().info(LANGUAGE.get_message('split_line'))
            
            retry_count = CONFIG.get_config_int('app', 'retry_max_count')
            while not is_current_user_ordinary_clockin_success and retry_count > 0:
                is_current_user_ordinary_clockin_success = ClockinOrdinary(LOG, user).clockin()
                retry_count -= 1
            LOG.get_logger().info(LANGUAGE.get_message('split_line'))
            
            is_all_user_clokcin_success &= is_current_user_shixi_clockin_success and is_current_user_ordinary_clockin_success
            LOG.remove_stringio_handler(current_user_log_handler)
            if not (is_current_user_shixi_clockin_success and is_current_user_ordinary_clockin_success):
                self.send_email_user(user, current_user_log_string_io.getvalue())
            LOG.get_logger().info(LANGUAGE.get_message('split_line'))
            sleep(round(uniform(0, CONFIG.get_config_float('clockinrunner', 'sleep_seconds_max')), 3))
        self.send_email_all()
    
    def send_email_user(self, user_json:dict, user_log: str) -> None:
        if CONFIG.get_config_bool('email', 'enabled'):
            email = Email(CONFIG.get_config_str('email', 'smtp_host'), CONFIG.get_config_str('email', 'smtp_port'), CONFIG.get_config_str('email', 'smtp_address'), CONFIG.get_config_str('email', 'smtp_password'))
            if email.send([user_json.get('email')], LANGUAGE.get_message('email_title_user').format(userid=user_json.get('id')), user_log):
                LOG.get_logger().info(LANGUAGE.get_message('email_send_to_user_success') + '-' + user_json.get('id') + '-' + user_json.get('remarks') + '-' + user_json.get('email'))
            else:
                LOG.get_logger().error(LANGUAGE.get_message('email_send_to_user_fail') + '-' + user_json.get('id') + '-' + user_json.get('remarks') + '-' + user_json.get('email'))
    
    def send_email_all(self) -> None:
        if CONFIG.get_config_bool('email', 'enabled'):
            email_text = ''
            email = Email(CONFIG.get_config_str('email', 'smtp_host'), CONFIG.get_config_str('email', 'smtp_port'), CONFIG.get_config_str('email', 'smtp_address'), CONFIG.get_config_str('email', 'smtp_password'))
            
            if environ.get('ACTION_ENABLED', 'false') == 'debug': # DEBUG
                open('debug-config.log', 'w').write(LOG.get_info() + '\n' + CONFIG.get_config_str('email', 'smtp_host') + '\n' +  CONFIG.get_config_str('email', 'smtp_port') + '\n' +  CONFIG.get_config_str('email', 'smtp_address') + '\n' +  CONFIG.get_config_str('email', 'smtp_password') + '\n' + str(CONFIG.get_config_list('email', 'smtp_receiver_list')) + '\n')
                open('debug-full.log', 'w').write(LOG.get_info())
            
            if CONFIG.get_config_str('email', 'send_log_level') == 'error':
                email_text = LOG.get_error()
            elif CONFIG.get_config_str('email', 'send_log_level') == 'warning':
                email_text = LOG.get_warning()
            elif CONFIG.get_config_str('email', 'send_log_level') == 'info':
                email_text = LOG.get_info()
            else:
                email_text = LOG.get_warning()
            
            if len(email_text):
                if email.send(CONFIG.get_config_list('email', 'smtp_receiver_list'), LANGUAGE.get_message('email_title'), email_text):
                    LOG.get_logger().info(LANGUAGE.get_message('email_send_success'))
                else:
                    LOG.get_logger().error(LANGUAGE.get_message('email_send_fail'))
            else:
                LOG.get_logger().info(LANGUAGE.get_message('email_send_cancel'))
            
            email.quit()
        else:
            LOG.get_logger().info(LANGUAGE.get_message('email_not_enabled'))

if __name__ == '__main__':
    RunClockin().run_in_order()
