
from typing import Callable 
import json 

def get_func_signature( func : Callable) -> dict :
    
    func_signature= {
        "name": func.__name__,
        "docstring": func.__doc__,
        "params": { "props":{}}

    }
    schema = {
        k: {"type": v.__name__} for k, v in func.__annotations__.items() if k != "return"
    }
    func_signature["params"]["props"] = schema
    return func_signature







def tool(func: Callable):
    def wrapper():
        func_signature = get_func_signature(func)
        return Tool(name=func_signature["name"], func=func, func_signature=json.dumps(func_signature))
    return wrapper

class Tool:
    def __init__(self, name: str, func: Callable, func_signature: str):
        self.name = name
        self.func = func
        self.func_signature = func_signature


    def run(self,**kwargs):
        return self.func(**kwargs)
    

    def __str__(self):
        return self.func_signature
    

