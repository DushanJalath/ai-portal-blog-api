from fastapi import APIRouter,Depends,HTTPException
from services import initial_service,get_blogs_byTags
from typing import List
from models import BlogPost



router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()

@router.get('/blogsByTags')
async def Blogs_By_tags(tags : List[int]):
    return get_blogs_byTags(tags)
