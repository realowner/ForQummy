from unittest import result
from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List

from models.secretdata import Secretdata, SecretdataIn
from repositories.secretdata import SecretdataRepository

from .depends import get_secretdata_repository


router = APIRouter()

@router.get('/', response_model=List[Secretdata])
async def read_secretdata(secretdata: SecretdataRepository=Depends(get_secretdata_repository),
                          limit: int=100, skip: int=0):
    return await secretdata.get_all(limit=limit, skip=skip)

@router.post('/', response_model=Secretdata)
async def create_secretdata(sd: SecretdataIn, secretdata: SecretdataRepository=Depends(get_secretdata_repository)):
    return await secretdata.create_sd(sd=sd)

@router.put('/', response_model=Secretdata)
async def update_secretdata(id: int, sd: SecretdataIn, secretdata: SecretdataRepository=Depends(get_secretdata_repository)):
    secret_data = await secretdata.get_by_id(id=id)
    if secret_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found!")
    return await secretdata.update_sd(id=id, sd=sd)

@router.delete('/')
async def delete_secretdata(id: int, secretdata: SecretdataRepository=Depends(get_secretdata_repository)):
    result = await secretdata.delete_sd(id=id)
    # if result is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found!")
    return {"status": True}