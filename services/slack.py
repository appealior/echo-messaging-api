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
        return model.SendResponse(success=True, error_message="")
    else:
        return model.SendResponse(success=False, error_message=resp.text)
