from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List

from models.users import User, UserIn
from repositories.users import UserRepository

from .depends import get_user_repository


router = APIRouter()
security = HTTPBasic()

@router.get('/', response_model=List[User])
async def read_users(users: UserRepository=Depends(get_user_repository), limit: int=100, skip: int=0):
    return await users.get_all(limit=limit, skip=skip)

@router.post('/', response_model=User)
async def create_user(user: UserIn, users: UserRepository=Depends(get_user_repository)):
    return await users.create(u=user)

@router.put('/', response_model=User)
async def update_user(id: int, user: UserIn, users: UserRepository=Depends(get_user_repository), 
                      credentials: HTTPBasicCredentials = Depends(security),):
    auth_result = await users.check_auth(credentials)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return await users.update(id=id, u=user)