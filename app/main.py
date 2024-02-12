
from fastapi import FastAPI,Response,HTTPException,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import database

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine)
app=FastAPI()

origins=[]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins    ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                          password='12345678',
                          cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print('successfully connected to database')
except Exception as error:
    print('failed to connect to database')
    print(f'Error:{error}') 
    
    
# @app.get('/sqlalchemy')
# def test_posts(db:Session=Depends(get_db)) :
#     posts=db.query(models.Post).all()
#     return{"data": posts}  
   
   # users paths
