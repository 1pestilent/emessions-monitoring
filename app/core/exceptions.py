from fastapi import HTTPException, status

incorrect_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect login or password",
    headers={"WWW-Authenticate": "Bearer"},
    )

user_inactive = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='User account is inactive'
    )