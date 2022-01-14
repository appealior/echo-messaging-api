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


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
