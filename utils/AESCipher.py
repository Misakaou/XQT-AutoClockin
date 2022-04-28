import base64
from Crypto.Cipher import AES

class AESCipher(object):
    __blocksize = None
    __iv = None
    __key = None
    __cipher = None

    def __init__(self, key:str, iv:str):
        self.__key = key.encode('utf-8')
        self.__iv = iv.encode('utf-8')
        self.__blocksize = AES.block_size

    def encrypt(self, raw:str):
        encrypt_bytes = AES.new(self.__key, AES.MODE_CBC, self.__iv).encrypt(self._pad_zero(raw))
        return str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    
    def decrypt(self, enc:str):
        decrypt_raw = AES.new(self.__key, AES.MODE_CBC, self.__iv).decrypt(base64.decodebytes(enc.encode("utf8"))).decode("utf8")
        return self._unpad_zero(decrypt_raw)

    def _pad_zero(self, string:str) -> bytes:
        return str.encode(string + (self.__blocksize - len(string) % self.__blocksize) * '\0')

    def _unpad_zero(self, string:str) -> str:
        return string.strip('\0')
    
if __name__ == '__main__':
    asecipher = AESCipher('woshiliangguofan', 'gnilaipojieshish')
    print(asecipher.encrypt('test raw data'))
    print(asecipher.decrypt('3IQ4ApzWgbGNQ0jsGHNB+A=='))
