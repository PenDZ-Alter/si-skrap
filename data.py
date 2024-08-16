import os
from dotenv import load_dotenv

class Data :
    # Protected Variables
    _payload = None
    _data_url = None
    _login_url = None
    _captcha_url = None
    
    def __init__(self) :
        load_dotenv()
        self._payload = {
            'username': os.getenv("USER"),
            'password': os.getenv("PASS"),
            'captcha_entered': '',
            'csrf_token' : ''
        }
        self._data_url = "https://siakad.uin-malang.ac.id/2.0/uin-PnjdwlnPmsrn"
        self._login_url = "https://siakad.uin-malang.ac.id/cek_login.php"
        self._captcha_url = "https://siakad.uin-malang.ac.id/captcha.php"
    
    def get_payload(self) :
        return self._payload
    
    def set_captcha_payload(self, value) :
        self._payload['captcha_entered'] = value
        
    def set_csrf_token_payload(self, value) : 
        self._payload['csrf_token'] = value
    
    def get_url(self) :
        return self._data_url
    
    def get_login(self) :
        return self._login_url
    
    def get_captcha(self) :
        return self._captcha_url