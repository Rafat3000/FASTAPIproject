# data validation
# pydantic :type hint 3.6

from pydantic import BaseModel



class ToDoSchema(BaseModel):
    title:str
    description : str
    complete:bool = False