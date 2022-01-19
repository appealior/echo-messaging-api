from fastapi.testclient import TestClient
from app.domain import route
from app.models import slack_model as model
from app.main import app

client = TestClient(app)

base_url = route.BASE_URL
slack_base = f'{base_url}{route.SLACK_BASE}'


def test_send_channel_message():
    payload = model.SendRequest(
        token="<Your oAuth Token>",
        message="pytest 1234!!"
    )
    resp = client.post(url=f'{slack_base}{route.SLACK_CHANNEL_SEND}', data=payload.json())

    assert resp.status_code == 200
    assert resp.json() == {"success": True, "error_message": ""}
