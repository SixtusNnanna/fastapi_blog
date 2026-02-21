from db.models.blog import Blog
from sqlalchemy.orm import Session
from schemas.blog import CreateBlog, UpdateBlog


def create_new_blog(blog: CreateBlog, db: Session, author_id: int = 1):
    blog = Blog(
        title=blog.title, slug=blog.slug, content=blog.content, author_id=author_id
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def retrieve_active_blogs(db: Session):
    active_blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return active_blogs


def update_new_blog(db: Session, blog: UpdateBlog, id: int, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {
            "error": f"Blog with {id} cannot be found"
        }
    
    if blog_in_db.author_id != author_id:
        return {
            "error": f"Only the author can edit blog with id {id}"
        }
    blog_in_db.title = blog.title
    blog_in_db.slug = blog.slug
    blog_in_db.content = blog.content
    db.commit()
    return blog_in_db


def delete_blog_by_id(db: Session, id: int, author_id: int):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog.first():
        return {"error": f"Could not find blog with id {id}"}
    if not blog.first().author_id == author_id:
        return {
            "error": "Only the author can delete a blog"
        }
    blog.delete()
    db.commit()
    return {"msg": f"Deleted blog with id {id}"}



