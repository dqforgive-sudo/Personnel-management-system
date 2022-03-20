from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.api import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import LimitOffsetPage, Page, add_pagination

app = FastAPI(title="三方人员管理系统API")


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# 管理员登陆
@app.post("/api/v1/login", response_model=schemas.Admin, tags=["登录相关"], summary="管理员登陆")
def login(admin_info: schemas.AdminBase, db: Session = Depends(get_db)):
    db_info = crud.vality_admin(db, admin_info=admin_info)
    if db_info is None:
        return HTTPException(status_code=400, detail="账号或密码错误")
    return db_info


# 创建正式员工信息
@app.post("/api/v1/sys/users/", response_model=schemas.User, tags=["正式员工相关"], description="创建正式员工信息",
          summary="创建正式员工信息")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_domain(db, domain=user.domain)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    return crud.create_user(db=db, user=user)


# 删除员工信息
@app.delete('/sys/user/{domain}', tags=["正式员工相关"], description="根据域账号删除员工信息", summary="删除员工信息")
def delete_user(domain: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, domain=domain)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"Msg": "Success", "Code": 200, "Data": "删除成功"}


# 根据域账号更新员工信息
@app.patch("/sys/user/profile", tags=["正式员工相关"], description="根据域账号更新员工信息", summary="根据域账号更新员工信息")
def update_user(domain: str, update_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, domain, update_user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"Msg": "Success", "Code": 200, "Data": "更新成功"}


# 查询所有正式员工信息
@app.get("/api/v1/users", response_model=Page[schemas.User], tags=["正式员工相关"], description="获取所有正式员工信息",
         summary="查询所有正式员工信息")
async def read_users(db: Session = Depends(get_db)):
    return paginate(db.query(models.User))


# 根据域账号查询员工信息
@app.get("/api/v1/users/{domain}", response_model=schemas.User, tags=["正式员工相关"], description="根据域账号查询员工信息",
         summary="根据域账号查询员工信息")
def read_user(domain: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, domain=domain)
    if db_user is None:
        raise HTTPException(status_code=200, detail="User not found")
    return db_user


# 创建三方人员信息
@app.post("/sys/tuser/tusers/", response_model=schemas.Item, tags=["三方员工相关"], description="创建三方人员信息",
          summary="创建三方人员信息")
def create_tuser(user: schemas.ItemCreate, db: Session = Depends(get_db)):
    json_user = user.dict()
    is_user_domain = crud.get_user_by_domain(db, domain=json_user["owner_name"])
    if is_user_domain:
        db_user = crud.get_item_by_domain(db, domain=user.domain)
        if db_user:
            raise HTTPException(status_code=400, detail="tuser already registered")
        return crud.create_item(db=db, user=user)
    raise HTTPException(status_code=400, detail="user not registered")


# 删除三方人员信息
@app.delete('/sys/tuser/{domain}', tags=["三方员工相关"], description="删除三方人员信息", summary="删除三方人员信息")
def delete_tuser(domain: str, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, domain=domain)
    if db_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"Msg": "Success", "Code": 200, "Data": "删除成功"}

# 根据域账号给正式员工添加三方员工信息
@app.post("/sys/user/tuser/", response_model=schemas.Item, tags=["正式员工相关"], description="根据域账号给正式员工添加三方员工信息",
          summary="根据域账号给正式员工添加三方员工信息")
def create_tuser_for_user(
        domain: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, domain=domain)

# 根据域账号更新正式员工名下的三方人员信息
@app.put("/sys/user/{domain}/", response_model=schemas.User, tags=["正式员工相关"], description="根据域账号更新正式员工名下的三方人员信息",
         summary="根据域账号更新正式员工名下的三方人员信息")
def relate_user_tuser(domain: str, ndomain: str, db: Session = Depends(get_db)):
    user = crud.relate_user_item(db=db, domain=domain, ndomain=ndomain)
    return user


# 查询所有三方员工信息
@app.get("/sys/tusers/page", response_model=List[schemas.Item], tags=["三方员工相关"], description="查询所有三方员工信息",
         summary="查询所有三方员工信息")
def read_tusers(pageNo: int = 0, pageSize: int = 10, db: Session = Depends(get_db)):
    users = crud.get_items(db, skip=pageNo, limit=pageSize)
    if len(users) > 0:
        return users
    else:
        raise HTTPException(status_code=400, detail="no data show")


# 根据域账号查询三方员工信息
@app.get("/sys/tuser/get", response_model=schemas.Item, tags=["三方员工相关"], description="根据域账号查询三方人员信息",
         summary="根据域账号查询三方员工信息")
def read_tuser(domain: str, db: Session = Depends(get_db)):
    db_user = crud.get_item_by_domain(db, domain=domain)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 根据域账号给正式员工添加三方员工信息
@app.post("/sys/user/tuser/", response_model=schemas.Item, tags=["正式员工相关"], description="根据域账号给正式员工添加三方员工信息",
          summary="根据域账号给正式员工添加三方员工信息")
def create_tuser_for_user(
        domain: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, domain=domain)


add_pagination(app)
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=1)
