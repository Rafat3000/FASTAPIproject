from fastapi import FastAPI
from schemas import ToDoSchema
import random
app = FastAPI()

all_todos={} #db

@app.get("/todos")
def todo_list():
    return [{"id":id , **todo} for id,todo in all_todos.items()]

@app.get("/todos/{todo_id}")
def todo_detail():
    pass

@app.put("/todos/{todo_id}")
def edit_todo():
    pass

@app.post("/todos")
def create_todo(todo:ToDoSchema):
    todo_id = random.randint(1,100) # generate unique id :id db
    all_todos[todo_id]=todo.model_dump() # data comming from APi
    return {"id":todo_id,**all_todos[todo_id]}

@app.delete("/todos/{todo_id}")
def delete_todo():
    pass






@app.get("/users") # url
def welcome(): # view
    return "Hello world"

@app.get("/transfer") 
def test():
    return "Generative AI"