from typing import Optional
from fastapi import FastAPI
from services import kakao, slack, telegram
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/slack/send/{message}')
def send_slack_message(message: str):
    """
    Slack 기본 메시지 전송
    :param message: 전송할 메시지
    :return: Response
    """
    res = slack.send_message(message=message)
    return res

@app.get('/kakao/init/')
def init_kakao(job: str, message: str):
    """
    Kakao Initialize 토큰이 없다면 카카오 Login > 동의하기 과정을 거친다.
    :param  job: selfMsg = 카카오톡 나에게 보내기
                 msg = 카카오톡 보내기(친구목록 불러오기로 이동)
    :param  message: 전송할 메시지
    """
    kakao.init_kakao(job, message)

@app.get('/kakao/login/')
def login_kakao(code: str):
    """
    Kakao Initialize 토큰이 없다면 카카오 Login > 동의하기 과정을 거친다.
    :param code: OAuth 인증키를 받아오는 parameter
    """
    kakao.login_kakao(code)

@app.get('/kakao/selfMsg/{message}')
def send_kakao_self_message(message: str):
    """
    최초 Initialize 시 전달했던 message 를 '나에게 보내기' 기능으로 전달한다.
    :param message: 전달할 메시지
    """
    res = kakao.send_kakao_self_message(message)
    return res

@app.get('/kakao/msg/{message}')
def send_kakao_message(message: str):
    """
    최초 Initialize 시 전달했던 message 를 '친구에게 보내기' 기능으로 전달한다.
    친구에게 보내기는 친구목록 불러오기를 선행해야한다.
    :param message: 전달할 메시지
    """
    res = kakao.send_kakao_message(message)
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
