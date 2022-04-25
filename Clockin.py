import json
from random import shuffle, randint
from time import sleep, time
import requests

from Config import Config
from utils.Email import Email
from utils.Language import Language
from utils.UAGetter import UAGetter
from utils.AESCipher import AESCipher
from utils.Log import Log

class Clockin:
    _user_json = None
    _clockin_url = None
    _clockin_method = None
    _clockin_data = None
    _clockin_header = None
    
    def __init__(self, user_json) -> None:
        self._user_json = user_json
        Log.logger.info(Language().get_message('clockin_start') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
        
    def clockin(self) -> bool:
        self._generate_data()
        if self._clockin_method == 'POST':
            Log.logger.info(Language().get_message('clockin_data') + '-' + str(self._clockin_data))
            try:
                response = requests.post(self._clockin_url, data=self._clockin_data, headers=self._clockin_header)
                if response.status_code == 200:
                    Log.logger.info(Language().get_message('clockin_server_response_success') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
                    Log.logger.info(Language().get_message('clockin_server_response') + '-' + response.text)
                    Log.logger.info(self._parase_response(response.text))
                else:
                    Log.logger.warning(Language().get_message('clockin_server_response_fail') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
                    Log.logger.warning(Language().get_message('clockin_server_response') + '-' + response.text)
                    Log.logger.warning(self._parase_response(response.text))
                self._send_email()
                return True
            except requests.ConnectionError:
                Log.logger.error(Language().get_message('error_connection'))
            except requests.HTTPError:
                Log.logger.error(Language().get_message('error_http'))
            except TimeoutError:
                Log.logger.error(Language().get_message('error_timeout'))
            except:
                Log.logger.error(Language().get_message('error_unknown'))
            return False
        elif self._clockin_method == 'GET':
            Log.logger.error(Language().get_message('request_method_not_support'))
            return False
        else:
            Log.logger.error(Language().get_message('request_method_not_support'))
            return False
    
    def _generate_data(self) -> None:
        pass
    
    def _parase_response(self, response_text) -> str:
        pass
    
    def _send_email(self) -> None:
        if Config().get_config_bool('email', 'enabled'):
            email = Email(Config().get_config_str('email', 'smtp_host'), Config().get_config_str('email', 'smtp_port'), Config().get_config_str('email', 'smtp_address'), Config().get_config_str('email', 'smtp_password'))
            if email.send(Config().get_config_list('email', 'email_receiver'), Language().get_message('email_title'), Log.log_stream.getvalue()):
                Log.logger.info(Language().get_message('email_send_success'))
            else:
                Log.logger.error(Language().get_message('email_send_fail'))
            email.quit()
    pass

class ShixiClockin(Clockin):    
    _name_longitude = None
    _name_latitude = None
    _name_temperature = None
    _name_verify = None
    
    def __init__(self, user_json) -> None:
        super().__init__(user_json)
        self._clockin_url = Config().get_config_str('clockinapi', 'shixi_qian_url')
        self._clockin_method = Config().get_config_str('clockinapi', 'shixi_qian_method')
        self._clockin_data = Config().get_config_json('clockinapi', 'shixi_qian_data')
        self._clockin_header = Config().get_config_json('clockinapi', 'shixi_qian_header')
        self._clockin_header['User-Agent'] = UAGetter().get_random_ua()
        
        self._name_temperature = Config().get_config_str('clockinapi', 'shixi_qian_temperature_field_name')
        self._name_longitude = Config().get_config_str('clockinapi', 'shixi_qian_longitude_field_name')
        self._name_latitude = Config().get_config_str('clockinapi', 'shixi_qian_latitude_field_name')
        self._name_verify = Config().get_config_str('clockinapi', 'shixi_qian_verify_field_name')
        
    def _generate_data(self) -> None:
        self._clockin_data[self._name_temperature] = '36.' + str(randint(1, 9))
        location = self.get_position_from_address_by_baidumap(self._user_json['address'])
        self._clockin_data[self._name_longitude] = location['lng']
        self._clockin_data[self._name_latitude] = location['lat']
        self._encrypt_verify()
        
    def _encrypt_verify(self) -> None:
        cipher = AESCipher(Config().get_config_str('shixiencrypt', 'shixi_qian_AES_KEY'), Config().get_config_str('shixiencrypt', 'shixi_qian_AES_IV'))
        self._clockin_data[self._name_verify] = cipher.encrypt(str(int(time())) + ',' + self._user_json['phone'])
        
    def get_position_from_address_by_baidumap(self, address) -> dict:
        try:
            return json.loads(requests.get(Config().get_config_str('baidumap', 'geocoding_url').format(address=address)).text)['result']['location']
        except:
            Log.logger.error(Language().get_message('error_baidumap') + '-' + address)
            return {'lng': '', 'lat': ''}
    
    def _parase_response(self, response_text) -> str:
        if not response_text:
            return None
        try:
            response_json = json.loads(response_text)
            if len(response_json) == 0:
                return Language().get_message('clockin_server_response_already_clockin') + '-' + str(response_json)
            elif response_json['code'] == 1:
                return Language().get_message('clockin_success')
            else:
                return Language().get_message('clockin_server_response_unknown') + '-' + str(response_json)
        except Exception:
            return Language().get_message('clockin_server_response_unknown') + '-' + str(response_text)   
    
    def clockin(self) -> bool:
        response_text = super().clockin()
        if response_text:
            if response_text == Config().get_config_str('clockinapi', 'shixi_qian_server_response_already_clockin'):
                Log.logger.warning(Language().get_message('clockin_server_response_already_clockin') +  '-' + response_text)
                return False
            else:
                return True
        else:
            return False


class ClockinOrdinary(Clockin):
    _name_id = None
    _name_temperature = None
    _name_province = None
    _name_city = None
    _name_district = None
    _name_address = None
    
    def __init__(self, user_json) -> None:
        super().__init__(user_json)
        self._clockin_url = Config().get_config_str('clockinapi', 'clockin_url')
        self._clockin_method = Config().get_config_str('clockinapi', 'clockin_method')
        self._clockin_data = Config().get_config_json('clockinapi', 'clockin_data')
        self._clockin_header = Config().get_config_json('clockinapi', 'clockin_header')
        self._clockin_header['User-Agent'] = UAGetter().get_random_ua()
        
        self._name_id = Config().get_config_str('clockinapi', 'clockin_id_field_name')
        self._name_temperature = Config().get_config_str('clockinapi', 'clockin_temperature_field_name')
        self._name_province = Config().get_config_str('clockinapi', 'clockin_province_field_name')
        self._name_city = Config().get_config_str('clockinapi', 'clockin_city_field_name')
        self._name_district = Config().get_config_str('clockinapi', 'clockin_district_field_name')
        self._name_address = Config().get_config_str('clockinapi', 'clockin_address_field_name')
        
    def _generate_data(self) -> None:
        self._clockin_data[self._name_temperature] = '36.' + str(randint(1, 9))
        self._clockin_data[self._name_id] = self._user_json['id']
        self._clockin_data[self._name_province] = self._user_json['province']
        self._clockin_data[self._name_city] = self._user_json['city']
        self._clockin_data[self._name_district] = self._user_json['district']
        self._clockin_data[self._name_address] = self._user_json['address']
    
    def _parase_response(self, response_text) -> str:
        if not response_text:
            return None
        try: 
            response_json = json.loads(response_text)
            if response_json['code'] == '200':
                return Language().get_message('clockin_success') + '-' + response_json['msg']
            elif response_json['code'] == '400':
                return Language().get_message('clockin_server_response_already_clockin') + '-' + str(response_json['msg'])
            else:
                return Language().get_message('clockin_server_response_unknown') + '-' + str(response_json)
        except Exception:
            return Language().get_message('clockin_server_response_unknown') + '-' + str(response_text)    
    
    def clockin(self) -> bool:
        return super().clockin()


if __name__ == '__main__': # Test
    user_list = [
                    {'id': '140502200000000000', 'phone': '19999999999', 'province': '山西省', 'city': '太原市', 'district': '小店区', 'address': '山西省太原市小店区CD写字楼', 'remarks': '张三'},
                    {'id': '140502200000000000', 'phone': '19999999999', 'province': '山西省', 'city': '太原市', 'district': '小店区', 'address': '山西省太原市小店区CD写字楼', 'remarks': '李四'},
                ]
    for user in user_list:
        ShixiClockin(user).clockin()
        ClockinOrdinary(user).clockin()
