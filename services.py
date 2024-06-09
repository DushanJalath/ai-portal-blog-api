from fastapi import HTTPException

def initial_service():
    return {"Ping":"Pong"}