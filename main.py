import requests
import json
import os

requests.packages.urllib3.disable_warnings()
SCKEY = os.environ['SCKEY']
email_list = os.environ['EMAIL']
email_list = json.loads(email_list)
password_list = os.environ['PASSWORD']
password_list = json.loads(password_list)
base_url_list = os.environ['BASE_URL']
base_url_list = json.loads(base_url_list)
msg_list = []


def checkin(email='', password='',
            base_url=''):
    email = email.split('@')
    email = email[0] + '%40' + email[1]

    session = requests.session()

    session.get(base_url, verify=False)

    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data, headers=headers, verify=False)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }

    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
    response = json.loads(response.text)
    print(response['msg'])
    return response['msg']

for i in range(0,len(email_list)):
    msg0 = '账户'+ str(i) + ' '+ str(email_list[i])
    msg1 = checkin(email=email_list[i],password=password_list[i],base_url=base_url_list[i])
    msg2 = msg0 + msg1
    msg_list.append(msg2)

if SCKEY != '':
    sendurl = 'https://sctapi.ftqq.com/' + SCKEY + '.send?title=机场签到&desp='+ str(msg_list)
    r = requests.post(url=sendurl)