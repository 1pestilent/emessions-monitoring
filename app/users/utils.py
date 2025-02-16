from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import session_dependency
from app.models.users import UserModel
from app.users.schemas import SafelyUserSchema, UserSchema, UserAddSchema
from app.core.security import hash_password

def return_safe_user(user: UserSchema) -> SafelyUserSchema:
    safe_user_data = user.model_dump(exclude={"password"})
    safe_user = SafelyUserSchema(**safe_user_data)
    return safe_user

async def get_user(
        session: session_dependency,
        username: str,
        ) -> UserSchema:
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user_from_db = result.scalars().first()
    if user_from_db is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Failed to get user!',
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    user = UserSchema.from_orm(user_from_db)
    return user

async def create_user(
        session: AsyncSession,
        user_add: UserAddSchema,
        ) -> int:
    new_user = UserModel(username = user_add.username,
                         email = user_add.email,
                         password = hash_password(user_add.password),
                         last_name = user_add.last_name,
                         first_name = user_add.first_name,
                         middle_name = user_add.middle_name
                         )
    
    session.add(new_user)
    await session.commit()

    await session.refresh(new_user)

    return new_user.id

async def user_is_uniq(
        session: AsyncSession,
        username: str,
        email: str,
):
    username_result = await session.execute(select(UserModel).where(UserModel.username == username))
    email_result = await session.execute(select(UserModel).where(UserModel.email == email))

    if username_result.scalars().first() or email_result.scalars().first() is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='Username or email is already busy!',
            headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        return True
    