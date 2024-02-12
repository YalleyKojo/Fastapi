from fastapi import APIRouter,Response,HTTPException,status,Depends
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix='/vote'
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def Vote(vote:schemas.Vote,db:Session=Depends(database.get_db),
         current_user:int=Depends(oauth2.get_current_user)):
    #get vote querry
    vote_querry=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                             models.Vote.user_id==current_user.id)
    found_vote=vote_querry.first()
    #check if the post has already been liked
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=
                                f'user{current_user.id} has already voted on post {vote.post_id}'
                                )
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id) 
        db.add(new_vote)
        db.commit()
        return{"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Vote does not exist")
        vote_querry.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully deleted vote"}            