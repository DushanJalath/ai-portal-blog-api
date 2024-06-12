from pydantic import BaseModel

class Comment(BaseModel):
    blogPost_id: str
    comment_id: str
    user_id: str
    comment: str

class Reply(BaseModel):
    blogPost_id: str
    comment_id: str
    reply_id: str
    reply: str    
    