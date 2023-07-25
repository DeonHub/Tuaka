
import datetime
import json

from .models import *
import environ



env = environ.Env()
environ.Env.read_env()

from .cookie import CookieManager
# COOKIE MANAGER CLASS

CM = CookieManager()

# COOKIE MANAGER CLASS 


LOGIN_COOKIE_NAME = "usercode"


# def login(request):
#     base_url = "https://db-api-v2.akwaabasoftware.com"

#     login_url = base_url + "/clients/login"

#     payload = json.dumps({
#         "phone_email": env('EMAIL'),
#         "password": env('PASSWORD')
#     })


#     headers = {
#     'Content-Type': 'application/json',
#     'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
#     }

#     response = requests.request("POST", login_url, headers=headers, data=payload).json()
#     CM.setcookie(request=request, cookie_name=LOGIN_COOKIE_NAME, cookie_value=response)

    # token = response['token']

    # return  { 'token': token, 'base_url': base_url }


    

# def counter(request):

#     now = datetime.datetime.now()
#     year = now.year

#     date = now.strftime("%A, %d %B, %Y")

#     time = now.strftime("%H:%M %p")

#     # print(client_name)
#     # print(unlimited)
    

#     # return {'total_members': total_members, 'client_name': client_name, 'organization': organization, 'branch':branch, 'unlimited': unlimited, 'date': date, 'time': time, 'year':year, 'new_id':new_id}
#     return { 'date': date, 'time': time, 'year':year }




def getClientDetails(request):

    today = datetime.datetime.now()
    # login_cookie_value = CM.getcookie(request=request, cookie_name=LOGIN_COOKIE_NAME)
    # print(login_cookie_value)


    try:
        login_cookie_value = CM.getcookie(request=request, cookie_name=LOGIN_COOKIE_NAME)

        if login_cookie_value is not None:
            details = json.loads(login_cookie_value) # since data saved in cookie is json
            code = details['code']

            # branch = details['branch']
            # pid = details['pid']
            # token = details['token']

            # try:
            #     base = Currency.objects.get(client_id=pid, base=True).currency
                
            # except:
            #     base = 'GHS'    

            # try:
            #     dasho = Dasho.objects.get(pid=pid)

            #     if dasho.redirected == True:
            #         setItem = True
            #     else:
            #         setItem = False
            # except:
            #     setItem = False  
        else:
            code = "False"
            raise Exception("Handle when no cookie value is found")


    except:
           code = "Falser"
        #    account_name = "Demoss Account"
        #    branch = "Other Branch"
        #    pid = 1
        #    setItem = False
        #    base = 'GHS'

    # print(pid)

    return { 'code': code }

