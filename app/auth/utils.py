from typing import Annotated, Union

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core import security
from app.core.config import (ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
                             TOKEN_TYPE_FIELD)
from app.auth import create_token
from app.models.database import session_dependency
from app.users.schemas import SafelyUserSchema, UserSchema
from app.users.utils import get_user, return_safe_user

oauth2_schemem = OAuth2PasswordBearer('/token')
http_bearer = HTTPBearer(auto_error=False)

async def authenticate_user(
        session: session_dependency,
        username: str,
        password: str,
        ) -> SafelyUserSchema:
    user: UserSchema = await get_user(session, username)
    if not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
            )

    return return_safe_user(user)

def get_token_payload(
        token: Annotated[str, Depends(oauth2_schemem)]
        ) -> dict:
    try: 
        payload = security.decode_jwt(token)
    except InvalidTokenError as e:
        return None
    return payload

def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    if not payload:
        return False
    
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    
    if not current_token_type == token_type:
        return False
    
    return True
    
def validate_token(
        token: str,
        token_type: str = ACCESS_TOKEN_TYPE,
) -> bool:
    payload = get_token_payload(token)

    if not payload:
        return False
    
    if not validate_token_type(payload,ACCESS_TOKEN_TYPE):
        return False
    
    return True
    
async def get_user_from_payload(
        payload: dict,
        session: session_dependency,
) -> SafelyUserSchema:
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username = payload.get("sub")
    user = await get_user(session, username)
    out_user = return_safe_user(user)
    return  out_user

def is_user_active(
    payload: dict,
) -> bool:
    is_active = payload.get("is_active")

    if is_active:
        return True
    
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='This user is not activated'
    )

async def get_current_user(
        payload: Annotated[dict, Depends(get_token_payload)],
        session: session_dependency,
) -> SafelyUserSchema:
    if validate_token_type(payload, ACCESS_TOKEN_TYPE):
        user = await get_user_from_payload(payload, session)
    if is_user_active:
        return user
    
async def get_current_user_from_token(
        token: str,
        session: session_dependency,
) -> SafelyUserSchema:
    payload = get_token_payload(token)

    if not validate_token(token):
        print(validate_token(token))
        raise HTTPException(status.HTTP_403_FORBIDDEN)
        
    user = await get_user_from_payload(payload, session)
    return user
    
async def get_current_user_for_refresh(
        payload: Annotated[dict, Depends(get_token_payload)],
        session: session_dependency,
) -> SafelyUserSchema:
    if validate_token_type(payload, REFRESH_TOKEN_TYPE):
        user = await get_user_from_payload(payload, session)
    if is_user_active:
        return user
    
async def get_new_access_token(
        session: session_dependency,
        refresh_token: str,
        ) -> Union[str, None]:
    payload = get_token_payload(refresh_token)
    if payload is not None:
        user = await get_user_from_payload(payload, session)
        return create_token.access_token(user)
    
    return False