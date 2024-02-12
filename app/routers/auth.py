from fastapi import APIRouter, Depends,status, HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas,models,utils,oauth2
router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    #OAuth2PasswordRequestForm will only return two things
    # username and password
    # {"username":email or username of the user, "password":Password of the user}
    user=db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    # verify if the input password is correct
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    #create a token 
    token=oauth2.create_access_token(data={"user_id":user.id})
    #return a token
    return {"access_token":token, "token_type":"bearer"}        