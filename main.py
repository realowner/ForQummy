from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from db.base import database
from endpoints import users, secretdata


def create_application(title):
    application = FastAPI(title=title)
    return application

app = create_application(title="ForQummy")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(secretdata.router, prefix="/secretdata", tags=["secretdata"])

templates = Jinja2Templates(directory="templates")

@app.on_event('startup')
async def startup():
    await database.connect()
    
@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app")