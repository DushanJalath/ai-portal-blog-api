import json
from fastapi import APIRouter,Depends,HTTPException

from models import Blog, Comment, Reply
from services import create_blog, initial_service, reply_comment, update_blog, get_blog_by_id, write_comment



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

@router.post('/write-comment', response_model=Comment)
async def writeComment(comment: Comment):
    return await write_comment(comment)

@router.post('/reply-comment', response_model=Reply)
async def replyComment(reply: Reply):
    return await reply_comment(Reply)

