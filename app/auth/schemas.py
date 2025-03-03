from fastapi import Form
from pydantic import BaseModel
from typing_extensions import Annotated

class UserLoginForm:
    def __init__(
            self,
            username: Annotated[str, Form()],
            password: Annotated[str, Form()],
            ):
        
        self.username = username
        self.password = password

class TokenSchema(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"