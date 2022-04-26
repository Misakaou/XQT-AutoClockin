import json
from random import shuffle, randint
from time import time
import requests

from Config import Config
from utils.Language import Language
from utils.UAGetter import UAGetter
from utils.AESCipher import AESCipher
from utils.Log import *

CONFIG = Config()
LANGUAGE = Language()

class Clockin:
    _user_json = None
    _clockin_url = None
    _clockin_method = None
    _clockin_data = None
    _clockin_header = None
    
    def __init__(self, user_json) -> None:
        self._user_json = user_json
        logger.info(LANGUAGE.get_message('clockin_start') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
    
    def clockin(self) -> bool:
        self._generate_data()
        if self._clockin_method == 'POST':
            logger.info(LANGUAGE.get_message('clockin_data') + '-' + str(self._clockin_data))
            try:
                response = requests.post(self._clockin_url, data=self._clockin_data, headers=self._clockin_header)
                if response.status_code == 200:
                    logger.info(LANGUAGE.get_message('clockin_server_response_success') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
                    logger.info(LANGUAGE.get_message('clockin_server_response') + '-' + response.text)
                else:
                    logger.warning(LANGUAGE.get_message('clockin_server_response_fail') + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
                    logger.warning(LANGUAGE.get_message('clockin_server_response') + '-' + response.text)
                self._parase_response(response.text)
                return True
            except requests.ConnectionError:
                logger.error(LANGUAGE.get_message('error_connection'))
            except requests.HTTPError:
                logger.error(LANGUAGE.get_message('error_http'))
            except TimeoutError:
                logger.error(LANGUAGE.get_message('error_timeout'))
            except:
                logger.error(LANGUAGE.get_message('error_unknown'))
            return False
        elif self._clockin_method == 'GET':
            logger.error(LANGUAGE.get_message('request_method_not_support'))
            return False
        else:
            logger.error(LANGUAGE.get_message('request_method_not_support'))
            return False
    
    def _generate_data(self) -> None:
        pass
    
    def _parase_response(self, response_text) -> None:
        pass
    pass

class ClockinShixi(Clockin):
    _name_longitude = None
    _name_latitude = None
    _name_temperature = None
    _name_verify = None
    
    def __init__(self, user_json) -> None:
        super().__init__(user_json)
        self._clockin_url = CONFIG.get_config_str('clockinapi', 'shixi_qian_url')
        self._clockin_method = CONFIG.get_config_str('clockinapi', 'shixi_qian_method')
        self._clockin_data = CONFIG.get_config_json('clockinapi', 'shixi_qian_data')
        self._clockin_header = CONFIG.get_config_json('clockinapi', 'shixi_qian_header')
        self._clockin_header['User-Agent'] = UAGetter().get_random_ua()
        
        self._name_temperature = CONFIG.get_config_str('clockinapi', 'shixi_qian_temperature_field_name')
        self._name_longitude = CONFIG.get_config_str('clockinapi', 'shixi_qian_longitude_field_name')
        self._name_latitude = CONFIG.get_config_str('clockinapi', 'shixi_qian_latitude_field_name')
        self._name_verify = CONFIG.get_config_str('clockinapi', 'shixi_qian_verify_field_name')
    
    def _generate_data(self) -> None:
        self._clockin_data[self._name_temperature] = '36.' + str(randint(1, 9))
        location = self.get_position_from_address_by_baidumap(self._user_json['address'])
        self._clockin_data[self._name_longitude] = location['lng']
        self._clockin_data[self._name_latitude] = location['lat']
        self._encrypt_verify()
    
    def _encrypt_verify(self) -> None:
        cipher = AESCipher(CONFIG.get_config_str('shixiencrypt', 'shixi_qian_AES_KEY'), CONFIG.get_config_str('shixiencrypt', 'shixi_qian_AES_IV'))
        self._clockin_data[self._name_verify] = cipher.encrypt(str(int(time())) + ',' + self._user_json['phone'])
    
    def get_position_from_address_by_baidumap(self, address) -> dict:
        try:
            return json.loads(requests.get(CONFIG.get_config_str('baidumap', 'geocoding_url').format(address=address)).text)['result']['location']
        except:
            logger.error(LANGUAGE.get_message('error_baidumap') + '-' + address)
            return {'lng': '', 'lat': ''}
    
    def _parase_response(self, response_text) -> None:
        if not response_text:
            return
        try:
            response_json = json.loads(response_text)
            if len(response_json) == 0:
                return logger.warning(LANGUAGE.get_message('clockin_server_response_already_clockin') + '-' + str(response_json) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
            elif response_json['code'] == 1:
                return logger.info(LANGUAGE.get_message('clockin_shixi_success'))
            else:
                return logger.warning(LANGUAGE.get_message('clockin_server_response_unknown') + '-' + str(response_json) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
        except Exception:
            return logger.error(LANGUAGE.get_message('clockin_server_response_unknown') + '-' + str(response_text) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])


class ClockinOrdinary(Clockin):
    _name_id = None
    _name_temperature = None
    _name_province = None
    _name_city = None
    _name_district = None
    _name_address = None
    
    def __init__(self, user_json) -> None:
        super().__init__(user_json)
        self._clockin_url = CONFIG.get_config_str('clockinapi', 'clockin_url')
        self._clockin_method = CONFIG.get_config_str('clockinapi', 'clockin_method')
        self._clockin_data = CONFIG.get_config_json('clockinapi', 'clockin_data')
        self._clockin_header = CONFIG.get_config_json('clockinapi', 'clockin_header')
        self._clockin_header['User-Agent'] = UAGetter().get_random_ua()
        
        self._name_id = CONFIG.get_config_str('clockinapi', 'clockin_id_field_name')
        self._name_temperature = CONFIG.get_config_str('clockinapi', 'clockin_temperature_field_name')
        self._name_province = CONFIG.get_config_str('clockinapi', 'clockin_province_field_name')
        self._name_city = CONFIG.get_config_str('clockinapi', 'clockin_city_field_name')
        self._name_district = CONFIG.get_config_str('clockinapi', 'clockin_district_field_name')
        self._name_address = CONFIG.get_config_str('clockinapi', 'clockin_address_field_name')
    
    def _generate_data(self) -> None:
        self._clockin_data[self._name_temperature] = '36.' + str(randint(1, 9))
        self._clockin_data[self._name_id] = self._user_json['id']
        self._clockin_data[self._name_province] = self._user_json['province']
        self._clockin_data[self._name_city] = self._user_json['city']
        self._clockin_data[self._name_district] = self._user_json['district']
        self._clockin_data[self._name_address] = self._user_json['address']

    def _parase_response(self, response_text) -> None:
        if not response_text:
            return
        try: 
            response_json = json.loads(response_text)
            if response_json['code'] == '200':
                return logger.info(LANGUAGE.get_message('clockin_success') + '-' + response_json['msg'])
            elif response_json['code'] == '400':
                return logger.warning(LANGUAGE.get_message('clockin_server_response_already_clockin') + '-' + str(response_json['msg']) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
            else:
                return logger.warning(LANGUAGE.get_message('clockin_server_response_unknown') + '-' + str(response_json) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])
        except Exception:
            return logger.error(LANGUAGE.get_message('clockin_server_response_unknown') + '-' + str(response_text) + '-' + self._user_json['remarks'] + '-' + self._user_json['id'])


if __name__ == '__main__': # Test
    user_list = [
                    {'id': '140502200000000000', 'phone': '19999999999', 'province': '山西省', 'city': '太原市', 'district': '小店区', 'address': '山西省太原市小店区CD写字楼', 'remarks': '张三'},
                    {'id': '140502200000000000', 'phone': '19999999999', 'province': '山西省', 'city': '太原市', 'district': '小店区', 'address': '山西省太原市小店区CD写字楼', 'remarks': '李四'},
                ]
    for user in user_list:
        ClockinShixi(user).clockin()
        ClockinOrdinary(user).clockin()
