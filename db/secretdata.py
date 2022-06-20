import sqlalchemy
from datetime import datetime

from .base import metadata


secretdata = sqlalchemy.Table(
    "secretdata", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("encrypted_text", sqlalchemy.String),
    sqlalchemy.Column("decrypted_text", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)