from typing import Optional
from pydantic import BaseModel


class SendRequest(BaseModel):
    token: str
    message: str


class SendResponse(BaseModel):
    success: bool
    error_message: Optional[str] = None
