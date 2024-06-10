import json
from typing import List
from fastapi import APIRouter,Depends,HTTPException
from models import Blog
from services import create_blog, delete_blog_by_id, get_all_blogs, initial_service, update_blog, get_blog_by_id



router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()


@router.get("/blog/{blog_id}")
async def get_blog_by_blog_id(blog_id: int):
    entity = await get_blog_by_id({"p_id": blog_id})
    return entity


@router.post('/createblog', response_model=Blog)
async def createBlog(blog: Blog):
    return await create_blog(blog)


@router.put('/updateblog{id}', response_model=Blog)
async def updateBlog(id: str, title:str, content:str):
    return await update_blog(id, title, content)


@router.get('/blogs', response_model=List[Blog])
async def getAllBlogs():
    return await get_all_blogs()


@router.delete('/blogs/{id}')
async def deleteBlog(id:str):
    return await delete_blog_by_id(id)


