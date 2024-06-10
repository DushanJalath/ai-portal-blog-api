import json
from fastapi import APIRouter,Depends,HTTPException
from services import get_blog_by_id
from services import initial_service


router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()

@router.get("/blog/{blog_id}")
async def get_blog_by_blog_id(blog_id: int):
    entity = await get_blog_by_id({"p_id": blog_id})
    return entity