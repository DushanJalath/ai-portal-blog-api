from fastapi import APIRouter,Depends,HTTPException
from services import initial_service, get_all_blogs, delete_blog_by_id
from pydantic import BaseModel
from typing import List
from models import Blog

router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()


# TODO: response_model need to be updated with the correct model - rtw
@router.get('/blogs', response_model=List[Blog])
async def getAllBlogs():
    return get_all_blogs()

@router.delete('/blogs/{id}')
async def deleteBlog(id:str):
    return delete_blog_by_id(id)