from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import requests
import json
import io

from login.models import TuakaUser
from .models import *
import datetime
from itertools import chain
from django.http import HttpResponse, HttpRequest 
import random
import string

import os
import environ

env = environ.Env()
environ.Env.read_env()





fee_url = "https://cash.akwaabasoftware.com/api"
super_url = "https://super.akwaabasoftware.com/api"

# fee_url = "http://127.0.0.1:8000/api"
# super_url = "http://127.0.0.1:7000/api"


def validate_fee_code(code):
    
    validate_url = f"{fee_url}/validate-code/{code}/"

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
    valid = requests.request("GET", validate_url, headers=headers).json()['success']

    if valid == "True":
        return True
    else:    
        return False



def validate_super_code(code):
    
    validate_url = f"{super_url}/validate-code/{code}/"

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
    valid = requests.request("GET", validate_url, headers=headers).json()['success']

    if valid == "True":
        return True
    else:    
        return False



def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))



def index(request, **kwargs):
    template_name = 'pay/index.html'
    code = kwargs.get('code')
    today = datetime.datetime.today()

    super_valid = validate_super_code(code)
   
    if super_valid == True:

        fees = False
        member_url = f"{super_url}/member-details/{code}/"

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        member = requests.request("GET", member_url, headers=headers).json()['data']


        email = member['email']

        try:
            info = TuakaUser.objects.get(email=email)
            info.verified = True
            info.usercode = code
            info.save()

            image = info.image

        except:
            image = ""


        data = MemberBusiness.objects.filter(usercode=code)

        return render(request, template_name, {
            'code': code,
            'member': member,
            'today': today,
            'data':data,
            'image': image,
        })


    else:
        messages.error(request, 'Invalid code. Please contact Admin') 
        return HttpResponseRedirect(reverse('login:login'))    






def viewBusiness(request, **kwargs):
    
    template_name = 'pay/view-business.html'
    code = kwargs.get('code')

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        clid = request.POST.get('client_id')


        items = []
        url = "https://db-api-v2.akwaabasoftware.com/members/login"
        payload = json.dumps({"phone_email": email, "password": password, "checkDeviceInfo": "on", "systemDevice": "1", "deviceType": "1", "deviceId": "1"})
        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
        key = requests.request("POST", url, headers=headers, data=payload).json()
        user = requests.request("POST", url, headers=headers, data=payload).json()

        for item in key.keys():
            items.append(item)

        if "non_field_errors" in items:  
            messages.error(request, 'Confirmation error. Incorrect email or password. ') 
            return redirect('pay:viewBusiness', code) 


        else: 
            token = key['token']
            mid = user['user']['id']

            client_id = user['user']['clientId']


            if int(client_id) == int(clid):
                
                # print('Success')

                url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"

                payload = json.dumps({})

                headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=CfbUldnaVD2hQH1UvaOPrtwWtoNtxabwC23rsdUagMO09OveIDpzVpdLtMRC0tfY; sessionid=zb3dn8vgge2e205gz4resy00oe3ayjwm'
                }

                response = requests.request("GET", url, headers=headers, data=payload).json()['data']

                client_name = response['name']

                

                # super_url = "https://super.akwaabasoftware.com/api"
                memberx_url = f"{super_url}/member-details/{code}/"

                headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

                suriname = requests.request("GET", memberx_url, headers=headers).json()['data']

                if suriname['middlename'] is not None:
                    member = suriname['firstname'] + ' ' + suriname['middlename'] + ' ' + suriname['surname'] 
                else:
                    member = suriname['firstname'] + ' ' + suriname['surname'] 


            
                try:
                    business = MemberBusiness.objects.get(client_id=client_id, member_id=mid)
                    business.client_name=client_name
                    business.member_name=member
                    business.usercode=code
                    business.save()
                except:
                    business = MemberBusiness.objects.create(client_id=client_id, member_name=member, member_id=mid, client_name=client_name, usercode=code)    
                    business.save()
                


                member_url = f"{fee_url}/update-usercode/"
                headers = {
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=ugVDmJWTsUSPEymPZ7fLtVC0Q8j6IeLG8TgyrkTe6IbLRbsFYEB89jLoB99sCzAZ; sessionid=vjnl5bhycfm5e1z1lb46jh06ec3nzunq'
                }

                payload = json.dumps({
                    "member_id": mid,
                    "usercode": code
                })


                try:
                    done = requests.request("POST", member_url, headers=headers, data=payload).json()['success']
                except:
                    done = "Not possible"  

                print(done)  


                messages.success(request, 'Confirmation successful. You have joined organization successfully.')
                return redirect('pay:index', code) 


            else:
                messages.error(request, 'Confirmation error. Not a member of chosen organization.')
                return redirect('pay:viewBusiness', code) 



    else:

        login_url = "https://db-api-v2.akwaabasoftware.com/clients/login"

        payload = json.dumps({ "phone_email":env('EMAIL'), "password": env('PASSWORD') })
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=ugVDmJWTsUSPEymPZ7fLtVC0Q8j6IeLG8TgyrkTe6IbLRbsFYEB89jLoB99sCzAZ; sessionid=vjnl5bhycfm5e1z1lb46jh06ec3nzunq'
        }

        token = requests.request("POST", login_url, headers=headers, data=payload).json()['token']



        url = "https://db-api-v2.akwaabasoftware.com/clients/code?datatable_plugin&length=1000"

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=ugVDmJWTsUSPEymPZ7fLtVC0Q8j6IeLG8TgyrkTe6IbLRbsFYEB89jLoB99sCzAZ; sessionid=vjnl5bhycfm5e1z1lb46jh06ec3nzunq'
        }

        clients = requests.request("GET", url, headers=headers, data=payload).json()['data']


        return render(request, template_name, {
            'code':code,
            'clients':clients,
        })





def account(request, **kwargs):
    template_name = 'pay/account.html'
    code = kwargs.get('code')
    pid = kwargs.get('pid')
    today = datetime.datetime.today()

    valid = validate_fee_code(code)

    if valid == True:

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        assigned_url = f"{fee_url}/assigned-fees/{code}/{pid}/"
        assigned_payments = requests.request("GET", assigned_url, headers=headers).json()['data']


        detail_url = f"{fee_url}/client-details/{pid}/"
        info = requests.request("GET", detail_url, headers=headers).json()['data']


        member_url = f"{fee_url}/member-details/{code}/"
        member = requests.request("GET", member_url, headers=headers).json()['data']

        member_id = member['member_id']

        
        currency_url = f"{fee_url}/base-currency/{pid}/"
        base = requests.request("GET", currency_url, headers=headers).json()['base']



        fees_url = f"{fee_url}/fee-types/{pid}/"
        fees = requests.request("GET", fees_url, headers=headers).json()



        expiry_url = f"{fee_url}/account-expiry/{member_id}/"

        try:
            expiry = requests.request("GET", expiry_url, headers=headers).json()['account_expiry']

            expiry = datetime.datetime.strptime(expiry, '%Y-%m-%d')
            string_expiry = expiry.strftime("%d %B, %Y")
        except:
            expiry = today 
            string_expiry = "None" 


        outstanding_url = f"{fee_url}/outstanding-bill/{member_id}/"
        total_bill = requests.request("GET", outstanding_url, headers=headers).json()['total_bill']
        start = requests.request("GET", outstanding_url, headers=headers).json()['start']
        end = requests.request("GET", outstanding_url, headers=headers).json()['end']



        return render(request, template_name, {
            'code': code,
            'info': info,
            'member': member,
            'base': base,
            'assigned_payments': assigned_payments,
            'today': today,
            'client_id':pid,
            'member_id': member_id,
            'fees':fees,
            'expiry': expiry,
            'string_expiry':string_expiry,
            'total_bill':total_bill,
            'start':start,
            'end':end,

        })

    else:
        messages.error(request, 'Invalid code. Please contact Admin') 
        return HttpResponseRedirect(reverse('login:login'))    








def load_bill(request):
    template_name = 'pay/bill.html'
    today = datetime.date.today()
    now = datetime.datetime.now()
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"

    url = f"{fee_url}/payment-link/"
    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}


    # print("Zm here")
    # response = "member"

    if request.method == "GET":

        branch = request.GET.get('branch')
        member_category = request.GET.get('member_category')
        group = request.GET.get('group')
        subgroup = request.GET.get('subgroup')
        member = request.GET.get('member')
        code = request.GET.get('code')
        invoice_type = request.GET.get('invoice_type')
        

        member_id = request.GET.get('member_id')

        fee_type_id = request.GET.get('fee_type_id')

        fee_description_id = request.GET.get('fee_description_id')

        outstanding_bill = request.GET.get('outstanding_bill')

        remarks = request.GET.get('remarks')
        user_type = request.GET.get('user_type')

        assigned_duration = request.GET.get('assigned_duration')
        expiration_bill = request.GET.get('expiration_bill')
        client_id = request.GET.get('client_id')


        install_range = request.GET.get('install_range')
        if install_range == "":
            install_range = "None"

        # print(install_range)    

        install_period = request.GET.get('install_period')
        if install_period == "":
            install_period = "None"

        # print(install_period) 


        total_amount_due = request.GET.get('total_amount_due')
        outstanding_balance = request.GET.get('outstanding_balance')

        if outstanding_balance == "":
                outstanding_balance = 0

        # print(outstanding_balance) 


        amount_paid = request.GET.get('amount_paid')
        payment_status = request.GET.get('payment_status')
        end_date = request.GET.get('end_date')

        if payment_status == 'full':
            arrears = 0
        else:    
            arrears=request.GET.get('arrears')

        invoice_id = request.GET.get('invoice_id')    

        platform = "tuaka"  
 

    
        payload = json.dumps({
            "branch": branch, 
            "member_category": member_category, 
            "group": group, 
            "subgroup": subgroup, 
            "member": member, 
            "member_id": member_id,

            "platform": platform,

            "fee_type_id": fee_type_id, 
            "fee_description_id": fee_description_id, 
            "outstanding_bill": outstanding_bill, 
            "remarks": remarks, 
            "user_type": user_type, 
            "assigned_duration": assigned_duration,

            "code": code,
            "expiration_bill": expiration_bill, 
            "client_id": client_id, 
            "install_range": install_range, 
            "install_period": install_period, 
            "total_amount_due": total_amount_due, 
            "outstanding_balance": outstanding_balance,
        
            "payment_status": payment_status,

            "amount_paid": amount_paid, 
            "end_date": end_date, 
            "arrears": arrears, 
            "invoice_id": invoice_id, 
            "invoice_type": invoice_type,

        })

        response = requests.request("POST", url, headers=headers, data=payload).json()['link']
        # response = requests.request("POST", url, headers=headers, data=payload).json()
        # print(response)

        # resp = member

        return render(request, template_name, {
            'response': response
            })
 
        # return render(request, template_name, {'response': response})

    



def load_outstanding(request):
    template_name = 'pay/outstanding.html'


    if request.method == "GET":
        amount = request.GET.get('amount')
        # amount = float(amount)

        client_id = request.GET.get('client_id')
        member_id = request.GET.get('member_id')
        usercode = request.GET.get('usercode')

        code = random.randint(10000, 99999)
        chars = random_char(3)
        invoice_no = f'{chars}{code}'
       

        url = "https://payproxyapi.hubtel.com/items/initiate"


        payload = json.dumps({
                "totalAmount": amount,
                "description": "Outstanding Fee Payment",
                "callbackUrl": "https://transactions.akwaabasoftware.com/add-transaction/",
                "returnUrl": f"https://transactions.akwaabasoftware.com/outstanding-transaction/outstandingPayment/{client_id}/{member_id}/{usercode}/",
                "merchantAccountNumber": "2017254",
                "cancellationUrl": "https://hubtel.com/",
                "clientReference": invoice_no
            })


        headers = {
            'Authorization': 'Basic UDc5RVdSVzozNmZmNzk3YTgyMjU0NzJmOTA2ZGU0NGM3NGVkZWE0Zg==',
            'Content-Type': 'application/json'
            }


        response = requests.request("POST", url, headers=headers, data=payload).json()['data']['checkoutUrl']

        
        return render(request, template_name, {'response': response})

    
   






def makePayments(request, **kwargs):
    
    template_name = 'pay/make-payment.html'
    pk = kwargs.get('pk')
    client_id = kwargs.get('pid')
    code = kwargs.get('code')


    valid = validate_super_code(code)

    if valid == True:

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        period_url = f"{fee_url}/periods/"
        periods = requests.request("GET", period_url, headers=headers).json()


        detail_url = f"{fee_url}/client-details/{client_id}/"
        info = requests.request("GET", detail_url, headers=headers).json()['data']

        


        fix_url = f"{fee_url}/fee-types/{client_id}/"
        fees = requests.request("GET", fix_url, headers=headers).json()


        descriptions_url = f"{fee_url}/fee-descriptions/{client_id}/"
        descriptions = requests.request("GET", descriptions_url, headers=headers).json()



        # detail_url = f"{fee_url}/client-details/{code}/"
        # info = requests.request("GET", detail_url, headers=headers).json()['data']


        assigned_url = f"{fee_url}/assigned-fees-by-id/{pk}/"
        assigned = requests.request("GET", assigned_url, headers=headers).json()['data']
        # print(assigned)

        
        member_url = f"{fee_url}/member-details/{code}/"
        member = requests.request("GET", member_url, headers=headers).json()['data']
        
        member_id = member['member_id']


        currency_url = f"{fee_url}/base-currency/{client_id}/"
        base = requests.request("GET", currency_url, headers=headers).json()['base']


        date = assigned['end_date']

        credit_url = f"{fee_url}/credit/member_id={member_id}/"
        credit = requests.request("GET", credit_url, headers=headers).json()['credit']


        today = datetime.date.today()
        last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
        year = datetime.datetime.now().year
        today = datetime.datetime.now()
        year = str(year) + "0000"


        return render(request, template_name, {
            'assigned': assigned, 
            'dated': date,  
            'periods': periods,
            'code':code,
            # 'company':organizations,
            'descriptions': descriptions,
            'fees': fees,
            'info': info,
            # 'base': base,
            # 'token': token,
            # 'member_account_name': member_account_name, 
            # 'member_branch':member_branch, 
            'mid':member_id, 
            'credit': credit,
            # 'token':token, 
            # 'setItem': setItem, 
            'base': base, 
            'clid':client_id
        })


    else:
        messages.error(request, 'Invalid code. Please contact Admin') 
        return HttpResponseRedirect(reverse('login:login'))    




def load_credit(request):
    template_name = 'pay/credit.html'


    if request.method == 'GET': 
        # member = request.GET.get('member')
        member_id = request.GET.get('member_id')


        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}


        credit_url = f"{fee_url}/credit/member_id={member_id}/"
        credit = requests.request("GET", credit_url, headers=headers).json()['credit']

        return render(request, template_name, {
            'credit': credit
            })






def load_breakdown(request):
    template_name = 'pay/breakdown.html'


    if request.method == 'GET': 
        # member = request.GET.get('member')
        assigned_id = request.GET.get('assigned_id')


        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        credit_url = f"{fee_url}/invoice-breakdown/{assigned_id}/"
        data = requests.request("GET", credit_url, headers=headers).json()['data']

        return render(request, template_name, {
            'data': data
            })






def load_amount_due(request):
    template_name = 'pay/amount_due.html'

    if request.method == 'GET': 
        assigned_id = request.GET.get('id')
        assigned_range = request.GET.get('range')
        assigned_period = request.GET.get('period')

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
        # amount-due/id=<str:id>/range=<str:range>/period=<str:period>/

        amount_url = f"{fee_url}/amount-due/id={assigned_id}/range={assigned_range}/period={assigned_period}/"
        total_amount_due = requests.request("GET", amount_url, headers=headers).json()['amount']

        return render(request, template_name, {
            'total_amount_due': total_amount_due
            })





def viewPayments(request, **kwargs):
    
    template_name = 'pay/view-payments.html'
    member_id = kwargs.get('mid')
    client_id = kwargs.get('pid')
    code = kwargs.get('code')

    valid = validate_fee_code(code)

    if valid == True:

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
        history_url = f"{fee_url}/history/{member_id}/{client_id}/"


        # detail_url = f"{fee_url}/client-details/{client_id}/"
        # info = requests.request("GET", detail_url, headers=headers).json()['data']


        currency_url = f"{fee_url}/base-currency/{client_id}/"
        base = requests.request("GET", currency_url, headers=headers).json()['base']


        fees_url = f"{fee_url}/fee-types/{client_id}/"
        fees = requests.request("GET", fees_url, headers=headers).json()


        detail_url = f"{fee_url}/client-details/{client_id}/"
        member_url = f"{fee_url}/member-details/{code}/"

        info = requests.request("GET", detail_url, headers=headers).json()['data']
        member = requests.request("GET", member_url, headers=headers).json()['data']


        # payments = MakePayment.objects.filter(member_id=member_id, confirmed=True).order_by('-id')
        payments = requests.request("GET", history_url, headers=headers).json()['data']

        # print(payments)

        return render(request, template_name, {
            'payments': payments,
            'code':code,
            'fees':fees,
            'info': info,
            'member': member,
            # 'base':base,
            # 'token': token,
            # 'member_account_name': member_account_name, 
            # 'member_branch':member_branch, 
            # 'mid':mid, 
            # 'token':token, 
            # 'setItem': setItem, 
            'base': base, 
            'clid':client_id
        })

    else:
        messages.error(request, 'Invalid code. Please contact Admin') 
        return HttpResponseRedirect(reverse('login:login'))  
