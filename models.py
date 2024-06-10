import datetime
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BlogPost(BaseModel): #represents a single blog post
    blogPost_id:UUID = Field(default_factory=uuid4, alias="_id") #primary key
    user_id:UUID #author`s user_id
    comment_constraint:bool #whether commenting is enabled or not, if enabled then true
    tags:List[int]  # List of integers indicating relavant tags (topics)
    number_of_views:int
    title:str #topic of the blog
    content:str #content of the blog : just texts here, didnt handle images/videos in the blog post
    postedAt:datetime = Field(default_factory=datetime.utcnow) #posted date time -utc time