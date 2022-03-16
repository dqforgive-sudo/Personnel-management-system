from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# 创建员工信息
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_domain(db, domain=user.domain)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    return crud.create_user(db=db, user=user)

# 查询所有员工信息
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    if len(users) > 0:
        return users
    else:
        raise HTTPException(status_code=400, detail="no data show")

# 根据域账号查询员工信息
@app.get("/users/{domain}", response_model=schemas.User)
def read_user(domain: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, domain=domain)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 根据域账号删除员工信息
@app.delete('/users/{domain}', response_model=schemas.User)
def delete_user(domain: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, domain=domain)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 根据域账号更新员工信息
@app.put("/users/{domain}", response_model=schemas.User)
def update_user(domain: str, update_user: schemas.UserUp, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, domain, update_user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# 根据域账号给正式员工添加三方员工信息
@app.post("/users/{domain}/items/", response_model=schemas.Item)
def create_item_for_user(
    domain: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, domain=domain)

# 获取所有三方员工信息
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# 根据域账号更新正式员工名下的三方人员信息
@app.put("/items/{domain}/", response_model=schemas.User)
def relate_user_item(domain: str, db: Session = Depends(get_db)):
    user = crud.relate_user_item(db=db, domain=domain)
    return user

# 更新三方人员信息
@app.put("/items/{domain}", response_model=schemas.Item)
def update_item(domain: str, update_item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_item(db, domain, update_item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# 删除三方人员信息
@app.delete('/items/{domain}', response_model=schemas.Item)
def delete_item(domain: str, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, domain=domain)
    if db_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_item


if __name__ == '__main__':
     uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True,debug=True,workers=1)