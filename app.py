from fastapi import FastAPI , Depends , Request , HTTPException
from schemas import ToDoSchemain ,ToDoSchemaout
from sqlalchemy import create_engine , Column , String , Boolean , Integer 
from sqlalchemy.orm import sessionmaker , Session 
from sqlalchemy.ext.declarative import declarative_base
from typing import List 
from fastapi.templating import Jinja2Templates 

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# SQLITE DB Settings
DATABASE_URL = "sqlite:///todo.db" # connection string 
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})# make the connection
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine) # open the connection
Base = declarative_base() # 


# design db tables
class ToDoModel(Base):
    __tablename__ = "todo"
    id = Column(Integer,primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean,default=False) # boolean 0 or 1


# create db tables
Base.metadata.create_all(bind=engine)


# function to create db session 
def get_db():
    db = SessionLocal()
    return db






@app.get("/todos",response_model =List[ToDoSchemaout])
def todo_list(db:Session = Depends(get_db)):
    return db.query(ToDoModel).all() # return all todos from sql-alchemy : select * from todo

@app.get("/todos/{todo_id}",response_model=ToDoSchemaout)
def todo_detail(todo_id:int,db:Session = Depends(get_db)):
    single_todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id).first()
    if single_todo is None:
        raise HTTPException(detail="Todo not found",status_code=404)
    return single_todo

@app.put("/todos/{todo_id}")
def edit_todo(todo_id: int, todo: ToDoSchemain, db: Session = Depends(get_db)):
    single_todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id).first()

    if single_todo is None:
        raise HTTPException(detail="Todo not found", status_code=404)

    # استخدم todo.dict() بدلاً من single_todo.dict()
    updated_data = todo.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(single_todo, key, value)

    db.commit()
    db.refresh(single_todo)
    return single_todo


@app.post("/todos",response_model =ToDoSchemaout)
def create_todo(todo:ToDoSchemain,db:Session = Depends(get_db)):
    new_todo = ToDoModel(**todo.model_dump())
    db.add(new_todo) # save in db :memory
    db.commit() # apply changes in db :harddisk
    db.refresh(new_todo) # current db object see new changes 
    return new_todo
    
    
    

@app.delete("/todos/{todo_id}",response_model=ToDoSchemaout)
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
    single_todo = db.query(ToDoModel).filter(ToDoModel.id == todo_id).first()

    if single_todo is None:
        raise HTTPException(detail="Todo not found",status_code=404)

    db.delete(single_todo)
    db.commit()
    return single_todo  # return json


@app.get("/all") # return List
def todos_list_template(request:Request,db:Session = Depends(get_db)):
    todos = db.query(ToDoModel).all()
    return templates.TemplateResponse("todos.html",{"request":request,"todos":todos})

