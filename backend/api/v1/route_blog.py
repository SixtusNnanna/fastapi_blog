from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db

from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, retrieve_active_blogs, update_new_blog, delete_blog_by_id
from db.models.user import User
from .route_login import get_current_user

router = APIRouter()


@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(blog, db, author_id=1)
    return blog


@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail="Blog with the {id} does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
    return blog


@router.get("", response_model=List[ShowBlog])
def get_active_blogs(db: Session = Depends(get_db)):
    active_blogs = retrieve_active_blogs(db=db)
    return active_blogs


@router.put("/{id}", response_model=ShowBlog)
def update_blog(blog: UpdateBlog, id: int, author_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = update_new_blog(db=db, blog=blog, id=id, author_id=current_user.id)
    if isinstance(blog, dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return blog

@router.delete("/{id}")
def delete_a_blog(id: int, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    message = delete_blog_by_id(db=db, id=id, author_id=current_user.id)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": message.get("msg")}


