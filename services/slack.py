from models import slack_model as model
import requests


def send_message(send_request: model.SendRequest):
    token = send_request.token
    channel = "#alarm_test"
    text = send_request.message

    resp = requests.post("https://slack.com/api/chat.postMessage",
                         headers={"Authorization": "Bearer " + token},
                         data={"channel": channel, "text": text})

    if resp.status_code == 200:
        return model.SendResponse(result_code=True)
    else:
        return model.SendResponse(result_code=False)


if __name__ == '__main__':
    req = model.SendRequest(token='xoxb-2955790037476-2938898660455-rz0HmxrR4NSOFEYJTCm9w1fJ', message='테스트 1010')
    res = send_message(req)
    print(res)
