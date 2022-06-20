from repositories.users import UserRepository
from repositories.secretdata import SecretdataRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)

def get_secretdata_repository() -> SecretdataRepository:
    return SecretdataRepository(database)