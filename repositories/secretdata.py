from sqlalchemy import insert
from .base import BaseRepository
from db.secretdata import secretdata
from models.secretdata import Secretdata, SecretdataIn

from typing import List, Optional

from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
import json


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
    
    # Достаем зашифрованные данные
    async def encrypted(self) -> List:
        response = requests.get('http://yarlikvid.ru:9999/api/top-secret-data') 
        return json.loads(response.text)
    
    # Добавление нескольких строк
    async def create_many(self, item_list: List) -> bool:
        items = await self.create_list(item_list)
        try:
            await self.database.execute_many(secretdata.insert(), items)
            return True
        except:
            return False

    # Вспомогательный метод для формирования данных для запроса
    async def create_list(self, items) -> List:
        item_list = []
        for item in items:
            item_list.append({
                'encrypted_text': item,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
        return item_list
    
    # Расшифруем данные
    async def decrypted(self, data: List) -> List:
        decrypted_list = []
        for item in data:
            encrypted_item = []
            parsed_item = Secretdata.parse_obj(item)
            encrypted_item.append(parsed_item.encrypted_text)
            decrypt = requests.post('http://yarlikvid.ru:9999/api/decrypt',
                                    auth=HTTPBasicAuth('qummy', 'GiVEmYsecReT!'),
                                    json=encrypted_item)
            query = secretdata.update().where(
                secretdata.c.encrypted_text==parsed_item.encrypted_text
            ).values(decrypted_text=json.loads(decrypt.text)[0])
            decrypted_list.append(json.loads(decrypt.text)[0])
            await self.database.execute(query=query)
        return decrypted_list
    
    # Отправляем репозиторий
    async def send_gitrepo(self, data: List):
        decrypted_list = []
        for item in data:
            parsed_item = Secretdata.parse_obj(item)
            decrypted_list.append(parsed_item.decrypted_text)
        my_info = {
            "name": "Сердюк Евгений",
            "repo_url": "https://github.com/realowner/ForQummy",
            "result": decrypted_list
        }
        send = requests.post('http://yarlikvid.ru:9999/api/result',
                                    auth=HTTPBasicAuth('qummy', 'GiVEmYsecReT!'),
                                    json=my_info)
        return my_info