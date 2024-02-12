from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title:str   
    content:str
    published: bool=True
    
    
class Post(PostBase):
    id:int
    
    class config:
        orm_mode=True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str   
    
class UserResponse(BaseModel):
    id:int
    email:EmailStr       
    
class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool=True
    created_at:datetime
    owner_id:int
    owner:UserResponse
    
    class config:
        orm_mode=True
    
    
        
class PostOut(BaseModel):
    Post:PostResponse
    votes:int
    
    class config:
        orm_mode=True
    
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str        
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
        
    