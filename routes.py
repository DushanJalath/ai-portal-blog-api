import json
from fastapi import APIRouter,Depends,HTTPException
from services import initial_service,get_blogs_byTags,create_blog, initial_service, update_blog, get_blog_by_id
from typing import List
from models import BlogPost




router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()



@router.get("/blog/{blog_id}")
async def get_blog_by_blog_id(blog_id: int):
    entity = await get_blog_by_id({"p_id": blog_id})
    return entity

@router.post('/createblog', response_model=BlogPost)
async def createBlog(blog: BlogPost):
    return await create_blog(blog)

@router.put('/updateblog{id}', response_model=BlogPost)
async def updateBlog(id: str, title:str, content:str):
    return await update_blog(id, title, content)


@router.get('/blogsByTags',response_model=List[BlogPost])
async def Blogs_By_tags(tags : List[int]):
    return await get_blogs_byTags(tags)

