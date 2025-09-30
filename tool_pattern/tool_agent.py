from groq import Groq 
from utils.utils import FixedChatHistory, build_prompt_structure,ChatHistory,chat_completion,build_chat_history,extract_tagged_content
import re ,json
from typing import Union
from tool_pattern.tool import Tool,validate_args
from colorama import Fore 


TOOL_AGENT_PROMPT = """
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
if the user query doesn't require any function calls, respond with an empty JSON object.
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

AGENT_RESPONSE_PROMPT = """
You are a helpful AI assistant. You have access to various tools and can provide comprehensive answers based on the information you gather. 

When responding to user queries:
- Provide natural, conversational responses
- Integrate information seamlessly into your answer
- Be direct and helpful
- Don't mention that you used tools or received "observations"
- Present the information as if you naturally know it
- If asked multiple questions, answer them all clearly and concisely

Your goal is to be helpful and provide accurate information in a natural, human-like manner.
"""

class ToolAgent:

    def process_tool_call(self, tool_calls: list[str]) -> Union[dict, None]:
        results = {}

        for tool_call_str in tool_calls:
            tool_call = json.loads(tool_call_str)
            if tool_call["name"] in self.tools_dict:
                validated_args = validate_args(tool_call, json.loads(self.tools_dict[tool_call["name"]].func_signature))
                tool = self.tools_dict[tool_call["name"]]
                result = tool.run(**validated_args)
                print(Fore.GREEN + f"Tool {tool_call['name']} executed with result: {result}" + Fore.RESET)
                results[tool_call["id"]] = result
            else:
                print(Fore.RED + f"Tool {tool_call['name']} not found." + Fore.RESET)

        return results


    def __init__(self,tools : Union[Tool,list[Tool]],model: str= "llama-3.3-70b-versatile")-> None:
        self.client = Groq() 
        self.model = model
        self.tools = tools if isinstance(tools,list) else [tools]
        self.tools_dict = {tool.name: tool for tool in self.tools}

    def add_tool_signatures_to_prompt(self,prompt : str) -> str:
        return prompt % ("".join(str(tool) for tool in self.tools))
    


    def run(self, query: str) -> str:
        
        prompt = self.add_tool_signatures_to_prompt(TOOL_AGENT_PROMPT)
        tool_history = FixedChatHistory()
        agent_history = FixedChatHistory()

        
        build_chat_history(tool_history,prompt,"system")    
        build_chat_history(tool_history,query,"user")
        
        
        build_chat_history(agent_history, AGENT_RESPONSE_PROMPT, "system")
        build_chat_history(agent_history,query,"user")

        response = chat_completion(self.client,tool_history,self.model)
        print(Fore.GREEN + "tool calling Agent response:" + Fore.RESET, response)

        tool_calls=extract_tagged_content(response,"tool_call")
        print(Fore.BLUE + "Extracted tool calls:" + Fore.RESET, tool_calls)

        if tool_calls : 
            results= self.process_tool_call(tool_calls)
            print(Fore.MAGENTA + "Tool call results:" + Fore.RESET, results)
            build_chat_history(agent_history,f'observations: {results}',"user")

        return Fore.CYAN + "Final agent response:" + Fore.RESET, chat_completion(self.client,agent_history,self.model)
    


            


   
        







   
   
