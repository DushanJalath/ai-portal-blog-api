from fastapi import APIRouter,Depends,HTTPException
from models import Blog
from services import create_blog, initial_service, update_blog



router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()

@router.post('/createblog', response_model=Blog)
async def createBlog(blog: Blog):
    return await create_blog(blog)

@router.put('/updateblog{id}', response_model=Blog)
async def updateBlog(id: str, title:str, content:str):
    return await update_blog(id, title, content)