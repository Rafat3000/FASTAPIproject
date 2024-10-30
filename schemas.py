# data validation
# pydantic :type hint 3.6

from pydantic import BaseModel


# create , update 
class ToDoSchemain(BaseModel):
    title:str
    description : str
    completed:bool = False

# get list , detail
class ToDoSchemaout(BaseModel):
    id: int 
    title:str
    description : str
    completed:bool = False


    class Config:
        from_attributes = True