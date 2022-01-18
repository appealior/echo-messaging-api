from fastapi import FastAPI
from services import kakao, slack, telegram
from domain import route
from models import kakao_model, slack_model
import uvicorn

base_url = route.BASE_URL
slack_base = f'{base_url}{route.SLACK_BASE}'
kakao_base = f'{base_url}{route.KAKAO_BASE}'

app = FastAPI()


@app.get(base_url)
def read_root():
    return {"Hello": "World"}


@app.post(f'{slack_base}{route.SLACK_CHANNEL_SEND}',
          response_model=slack_model.SendResponse,
          summary="Slack 채널 메시지 전송")
async def send_slack_message(send_request: slack_model.SendRequest):
    """
    Slack 채널 메시지 전송
    :param send_request: 요청 모델
    :return:
    """
    response = slack.send_message(send_request)
    return response


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
    base_url = route.BASE_URL
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
