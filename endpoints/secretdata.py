from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from models.secretdata import Secretdata, SecretdataIn
from repositories.secretdata import SecretdataRepository

from .depends import get_secretdata_repository, get_user_repository
from .users import security
from repositories.users import UserRepository


router = APIRouter()

@router.get('/', response_model=List[Secretdata])
async def read_secretdata(secretdata: SecretdataRepository=Depends(get_secretdata_repository),
                          users: UserRepository=Depends(get_user_repository),
                          credentials: HTTPBasicCredentials = Depends(security),
                          limit: int=100, skip: int=0):
    auth_result = await users.check_auth(credentials)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return await secretdata.get_all(limit=limit, skip=skip)

@router.post('/', response_model=Secretdata)
async def create_secretdata(sd: SecretdataIn, secretdata: SecretdataRepository=Depends(get_secretdata_repository),
                            users: UserRepository=Depends(get_user_repository),
                            credentials: HTTPBasicCredentials = Depends(security)):
    auth_result = await users.check_auth(credentials)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return await secretdata.create_sd(sd=sd)

@router.put('/', response_model=Secretdata)
async def update_secretdata(id: int, sd: SecretdataIn, secretdata: SecretdataRepository=Depends(get_secretdata_repository),
                            users: UserRepository=Depends(get_user_repository),
                            credentials: HTTPBasicCredentials = Depends(security)):
    auth_result = await users.check_auth(credentials)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    secret_data = await secretdata.get_by_id(id=id)
    if secret_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found!")
    return await secretdata.update_sd(id=id, sd=sd)

@router.delete('/')
async def delete_secretdata(id: int, secretdata: SecretdataRepository=Depends(get_secretdata_repository),
                            users: UserRepository=Depends(get_user_repository),
                            credentials: HTTPBasicCredentials = Depends(security)):
    auth_result = await users.check_auth(credentials)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    secret_data = await secretdata.get_by_id(id=id)
    if secret_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found!")
    result = await secretdata.delete_sd(id=id)
    if result:
        return {"status": True}
    return {"status": False}