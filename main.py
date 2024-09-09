from http.client import HTTPException
from importlib.metadata import files
from unicodedata import name
from urllib.request import Request
from xml.etree.ElementInclude import include
from fastapi import FastAPI
from exceptions import StoryException
from router import blog_get, blog_post, user, article, product, file
from auth import authentication
from db.database import engine
from db import models
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get('/hello')
def index():
    return {'message': 'Hello World!'}

@app.exception_handler(StoryException)
def story_eception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

@app.exception_handler(HTTPException)
def custom_handler(request: Request, exc: StoryException):
    return PlainTextResponse(str(exc), status_code=400)
    
models.Base.metadata.create_all(engine)

app.mount('/files', StaticFiles(directory="files"), name='files')
