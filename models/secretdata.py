from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import datetime


class Secretdata(BaseModel):
    id: Optional[int]
    encrypted_text: str
    decrypted_text: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class SecretdataIn(BaseModel):
    encrypted_text: str
    decrypted_text: str