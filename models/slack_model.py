from pydantic import BaseModel


class SendRequest(BaseModel):
    token: str
    message: str


class SendResponse(BaseModel):
    result_code: bool
