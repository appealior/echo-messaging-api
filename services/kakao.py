import requests
import webbrowser
import json

KAKAO_GET_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
APP_KEY = '31608a4cce72d2278dcc31afdcc7e8ee'
REDIRECT_HOST = 'http://127.0.0.1:8000/kakao/login/'
INIT_MESSAGE = ''
NEXT_JOB = ''
ACCESS_TOKEN = ''
KAKAO_HEADER = {}

def init_kakao(job: str, message: str):

    url = f'https://kauth.kakao.com/oauth/authorize?client_id={APP_KEY}&redirect_uri={REDIRECT_HOST}&response_type=code'
    global INIT_MESSAGE
    INIT_MESSAGE = message
    global NEXT_JOB
    NEXT_JOB = job
    webbrowser.open(url)
    # rs = requests.get(url)
    # print(rs.url)

def login_kakao(code: str):
    data = {
        'grant_type': 'authorization_code',
        'client_id': APP_KEY,
        'redirect_uri': REDIRECT_HOST,
        'code': code,
    }
    response = requests.post(KAKAO_GET_TOKEN_URL, data=data)
    tokens = response.json()
    global ACCESS_TOKEN
    ACCESS_TOKEN = tokens['access_token']
    global KAKAO_HEADER
    KAKAO_HEADER = {
        "Authorization": "Bearer " + ACCESS_TOKEN
    }

    if NEXT_JOB == 'selfMsg':
        response = requests.get(url=f'http://127.0.0.1:8000/kakao/selfMsg/{INIT_MESSAGE}')

    elif NEXT_JOB == 'msg':
        response = requests.get(url=f'http://127.0.0.1:8000/kakao/msg/{INIT_MESSAGE}')
    return response.json()


def send_kakao_self_message(message: str):
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": "나에게 보내기 테스트입니다. 보낸 메시지는 - " + message,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            },
            "button_title": "바로 확인"})
    }
    response = requests.post('https://kapi.kakao.com/v2/api/talk/memo/default/send', headers=KAKAO_HEADER, data=data)
    return {"result": response.status_code, "kakao_resultCode": response.json()['result_code'], "sendMessage": message}

def send_kakao_message(message: str):
    response = requests.get('https://kapi.kakao.com/v1/api/talk/friends', headers=KAKAO_HEADER)
    print(response)
    print(response.json())
    # friendsArray = response.json()['elements']
    # print(friendsArray)
    # return response.json()

    # data = {
    #     "template_object": json.dumps({
    #         "object_type": "text",
    #         "text": "나에게 보내기 테스트입니다. 보낸 메시지는 - " + INIT_MESSAGE,
    #         "link": {
    #             "web_url": "https://developers.kakao.com",
    #             "mobile_web_url": "https://developers.kakao.com"
    #         },
    #         "button_title": "바로 확인"})
    # }
    # response = requests.post('https://kapi.kakao.com/v2/api/talk/memo/default/send', headers=headers, data=data)
    # return {"result": response.status_code, "kakao_resultCode": response.json()['result_code'], "sendMessage": INIT_MESSAGE}