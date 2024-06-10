from fastapi import APIRouter,Depends,HTTPException
from models import Blog
from services import create_blog, initial_service, update_blog



router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()

@router.post('/createblog', response_model=Blog)
async def createBlog(blog: Blog):
    response = await create_blog(blog)
    if response:
        return response

@router.put('/updateblog{id}', response_model=Blog)
async def updateBlog(id: str, title:str, content:str):
    response = await update_blog(id, title, content)
    if response:
        return response