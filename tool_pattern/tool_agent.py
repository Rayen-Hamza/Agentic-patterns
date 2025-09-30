from groq import Groq 
from utils.utils import *
import re ,json
from typing import Union
from tool_pattern.tool import Tool


TOOL_AGENT_PROMPT = """
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
For each function call return a json object with function name and arguments within <tool_call></tool_call>
XML tags as follows:

<tool_call>
{"name": <function-name>,"arguments": <args-dict>,  "id": <monotonically-increasing-id>}
</tool_call>

Here are the available tools:

<tools>
%s
</tools>
"""

class ToolAgent:

    def parse_tool_call(self,tool_call_str: str):
        pattern = r'</?tool_call>'
        clean_tags = re.sub(pattern, '', tool_call_str)
        
        try:
            tool_call_json = json.loads(clean_tags)
            return tool_call_json
        except json.JSONDecodeError:
            return clean_tags
        except Exception as e:
            print(f"Unexpected error: {e}")


    def __init__(self,tools : Union[Tool,list[Tool]],model: str= "llama-3.3-70b-versatile")-> None:
        self.client = Groq() 
        self.model = model
        self.tools = tools if isinstance(tools,list) else [tools]
        self.tools_dict = {tool.name: tool for tool in self.tools}

    def add_tool_signatures_to_prompt(self,prompt : str) -> str:
        return prompt % ("".join(str(tool) for tool in self.tools))


    def run(self, query: str):
        pass




   
   
