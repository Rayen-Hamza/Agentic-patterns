
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




def validate_args(tool_call : dict , tool_signature: dict) -> dict:
    validated_args = {}
    for param, details in tool_signature["params"]["props"].items():
        if param in tool_call["arguments"]:
            arg_value = tool_call["arguments"][param]
            expected_type = details["type"]
            if expected_type == "int":
                validated_args[param] = int(arg_value)
            elif expected_type == "float":
                validated_args[param] = float(arg_value)
            elif expected_type == "str":
                validated_args[param] = str(arg_value)
            elif expected_type == "bool":
                if isinstance(arg_value, bool):
                    validated_args[param] = arg_value
                elif isinstance(arg_value, str):
                    if arg_value.lower() in ['true', '1', 'yes']:
                        validated_args[param] = True
                    elif arg_value.lower() in ['false', '0', 'no']:
                        validated_args[param] = False
                    else:
                        raise ValueError(f"Cannot convert {arg_value} to bool")
                else:
                    raise ValueError(f"Cannot convert {arg_value} to bool")
            else:
                raise ValueError(f"Unsupported type: {expected_type}")
        else:
            raise ValueError(f"Missing argument: {param}")
    return validated_args



def tool(func: Callable):
    func_signature = get_func_signature(func)
    return Tool(name=func_signature["name"], func=func, func_signature=json.dumps(func_signature))




class Tool:
    def __init__(self, name: str, func: Callable, func_signature: str):
        self.name = name
        self.func = func
        self.func_signature = func_signature


    def run(self,**kwargs):
        return self.func(**kwargs)
    

    def __str__(self):
        return self.func_signature
    

