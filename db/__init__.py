from .secretdata import secretdata
from .users import users

from .base import engine, metadata


metadata.create_all(bind=engine)