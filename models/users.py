from pydantic import BaseModel, validator
from typing import Optional

import datetime


class User(BaseModel):
    id: Optional[str] = None
    username: str
    password_hash: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class UserIn(BaseModel):
    username: str
    password: str
    password2: str
    
    @validator("password2")
    def password_match(cls, val, values):
        if 'password' in values and val != values['password']:
            raise ValueError('Passwords dont match')
        return val