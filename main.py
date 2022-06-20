from fastapi import FastAPI
import uvicorn

from db.base import database
from endpoints import users, secretdata


def create_application(title):
    application = FastAPI(title=title)
    return application

app = create_application(title="ForQummy")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(secretdata.router, prefix="/secretdata", tags=["secretdata"])

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app")