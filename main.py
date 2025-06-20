from fastapi import FastAPI,Depends,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,EmailStr
from typing import Annotated


from database import Base  
from database import engine,Sessionlocal
from sqlalchemy.orm import Session
from models import User


class UserCreate(BaseModel):
    
   
    name: Annotated[str,Field(...,description='Enter the name of the patient')]
    age:Annotated[int,Field(...,description='Enter the age of the patient')]
    email: EmailStr
    
    
    
app=FastAPI()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        timeout_graceful_shutdown=10  
    )

Base.metadata.create_all(engine)


def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()  
    
@app.get("/")
def hello():
    return{"meaasge":"Hello"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    
        users = db.query(User).all()
        return users


@app.post("/create")

def add(user:UserCreate,db: Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    updated_user: UserCreate,  
    db: Session = Depends(get_db)
):
   
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")


    existing_user.name = updated_user.name
    existing_user.age = updated_user.age
    existing_user.email = updated_user.email

 
    db.commit()
    db.refresh(existing_user)
    return existing_user
    

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_to_delete)
    db.commit()
    return JSONResponse(status_code=200,content={"message":"patient deleted successfully"})
    