from fastapi import APIRouter,Response,HTTPException,status,Depends
from sqlalchemy.orm import Session

from app import oauth2
from .. import schemas,models,utils
from ..database import engine,get_db 

router=APIRouter()
@router.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def createUser(user:schemas.UserCreate,db:Session=Depends(get_db)):
    
    #hash password
     hashed_password=utils.hash(user.password)
     #save hashed password as new password
     user.password=hashed_password
   
     new_user=models.User(**user.model_dump())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user 
       
@router.get("/users/{id}",response_model=schemas.UserResponse) 
def getUser(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    user=db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id:{id} does not exist')
    return user   
   
    