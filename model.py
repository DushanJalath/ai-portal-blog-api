from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List
from datetime import datetime

class BlogPost(BaseModel): #represents a single blog post
    blogPost_id:UUID = Field(default_factory=uuid4, alias="_id") #primary key
    user_id:UUID #author`s user_id
    comment_constraint:bool #whether commenting is enabled or not if enabled then true
    tags:List[int]  # List of integers indicating relavant tags (topics)
    number_of_views:int
    title:str #topic of the blog
    content:str #content of the blog : just texts here, didnt handle images/videos in the blog post
    postedAt:datetime = Field(default_factory=datetime.utcnow) #posted date time -utc time

class Comment(BaseModel):
    comment_id:UUID = Field(default_factory=uuid4, alias="_id") #primary key
    user_id:UUID #commenting person`s user_id
    blogPost_id:UUID 
    text:str #comment content
    commentedAt:datetime = Field(default_factory=datetime.utcnow) #commented date time -utc time

class Reply(BaseModel):
    reply_id:UUID = Field(default_factory=uuid4, alias="_id") #primary key
    parentContent_id:UUID #either a comment_id or reply_id (when someone reply to an existing reply)
    user_id:UUID #replying person`s` user_id
    text:str #reply content
    repliedAt:datetime = Field(default_factory=datetime.utcnow) #replied date time -utc time

