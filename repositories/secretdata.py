from .base import BaseRepository
from db.secretdata import secretdata
from models.secretdata import Secretdata, SecretdataIn

from typing import List, Optional

from datetime import datetime


class SecretdataRepository(BaseRepository):
    
    # Достаем все
    async def get_all(self, limit: int=100, skip: int=0) -> List[Secretdata]:
        query = secretdata.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)
    
    # Достаем по id
    async def get_by_id(self, id: int) -> Optional[Secretdata]:
        query = secretdata.select().where(secretdata.c.id==id)
        secret_data = await self.database.fetch_one(query)
        if secret_data is None:
            return None
        return Secretdata.parse_obj(secret_data)
    
    # Создаем данные
    async def create_sd(self, sd: SecretdataIn) -> Secretdata:
        secret_data = Secretdata(
            encrypted_text = sd.encrypted_text,
            decrypted_text = sd.decrypted_text,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )
        values = {**secret_data.dict()}
        values.pop("id", None)
        values.pop("decrypted_text", None)
        query = secretdata.insert().values(**values)
        secret_data.id = await self.database.execute(query=query)
        return secret_data
    
    # Обновляем данные
    async def update_sd(self, id: int, sd: SecretdataIn) -> Secretdata:
        secret_data = Secretdata(
            id=id,
            encrypted_text = sd.encrypted_text,
            decrypted_text = sd.decrypted_text,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )
        values = {**secret_data.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        values.pop("encrypted_text", None)
        query = secretdata.update().where(secretdata.c.id==id).values(**values)
        await self.database.execute(query=query)
        return secret_data
    
    # Удаляем данные
    async def delete_sd(self, id: int) -> bool:
        try:
            query = secretdata.delete().where(secretdata.c.id==id)
            await self.database.execute(query=query)
            return True
        except:
            return False
        