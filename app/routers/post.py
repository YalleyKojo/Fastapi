from fastapi import APIRouter,Response,HTTPException,status,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from .. import schemas,models,oauth2
from ..database import engine,get_db

router=APIRouter()

@router.get("/posts",response_model=List[schemas.PostOut])
def posts(db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user),
          skip:int=0, limit:int=10,search:Optional[str]=""):
    # cursor.execute("""
    #                Select * from post
    #                """)
    # posts=cursor.fetchall()
    # posts=db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/posts/{id}",response_model=schemas.PostResponse)
def get_post(id:int,db:Session=Depends(get_db),
             current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                Select * from post where id=%s
    #                """,(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this operation')    
    return  post
    

@router.post('/createpost',response_model=schemas.PostResponse)
def createPost(post:schemas.PostBase,db:Session=Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                Insert into post (title,content,publish) values
    #                (%s,%s,%s) returning *
    #                """,(post.title,post.content,post.publish))
    # new_post=cursor.fetchone()
    # conn.commit()
    # new_post=models.Post(title=post.title,content=post.content,published=post.publish)
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/posts/{id}',response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.Post,db:Session=Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(
    #     """
    #     Update post set title=%s,content=%s,publish=%s where id=%s
    #     returning *
    #     """
    # ,(post.title,post.content,post.publish,str(id)))
    # updated=cursor.fetchone()
    # conn.commit()
    updated_querry=db.query(models.Post).filter(post.id==id)
    updated=updated_querry.first()
    if updated == None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist'
                            )
    if updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'You are not authorized to perform this operation')
    updated_querry.update(post.model_dump(),synchronize_session=False)  
    db.commit()  
    return updated

@router.delete('/posts/{id}',response_model=schemas.PostResponse)
def deletepost(id:int,db:Session=Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """
    #     Delete from post where id=%s
    #     returning *
    #     """ 
    # ,(str(id)))
    
    # deleted=cursor.fetchone()
    # conn.commit()
    
    post_querry=db.query(models.Post).filter(models.Post.id == id)
    post=post_querry.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this operation')
    post_querry.delete(synchronize_session=False) 
    db.commit()   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   
