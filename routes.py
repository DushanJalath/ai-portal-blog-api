from fastapi import APIRouter,Depends,HTTPException
from services import initial_service



router=APIRouter()

@router.get('/')
async def getInitial():
    return initial_service()