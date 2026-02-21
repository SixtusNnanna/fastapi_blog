from typing import Optional
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db

from db.repository.blog import retrieve_active_blogs, retrieve_blog

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = retrieve_active_blogs(db=db)
    context = {"request": request, "blogs": blogs, "alert": alert}
    return templates.TemplateResponse("blogs/home.html", context=context)


@router.get("/app/blog/{id}/")
def blog_details(request: Request, id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    context = {"request": request, "blog": blog}
    return templates.TemplateResponse("blogs/detail.html", context=context)
