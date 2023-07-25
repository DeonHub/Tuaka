import base64
import datetime
from django.shortcuts import render
import requests
import json
# COOKIE MANAGER IMPORTS
from django.http import HttpResponse, HttpRequest 
# COOKIE MANAGER CLASS


class CookieManager(object):
    template_name = ""
    def __init__(self,):
        super(CookieManager, self).__init__()
        
    def setcookie(self, request: HttpRequest, cookie_name: str, cookie_value):  
        response = HttpResponse()  

        cookie_str_value = base64.b64encode(cookie_value.encode('utf-8')).decode('utf-8')

        response.set_cookie(key=cookie_name, value=cookie_str_value) 
        # print(response.COOKIES)

        return response  


    def getcookie(self, request: HttpRequest, cookie_name: str,): 
        # print(f"Cookie name at get is {cookie_name}")
        # print(request.COOKIES)


        if cookie_name in request.COOKIES:
            cookie_str_value = request.COOKIES[cookie_name]
            cookie_str_value = f'{cookie_str_value}=='
            cookie_value = base64.b64decode(cookie_str_value.encode('utf-8').strip()).decode('utf-8')
            # print(cookie_value)
            return cookie_value 

        return None


