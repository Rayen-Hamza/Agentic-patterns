import json
import re 
from typing import List, Union

from utils import  build_prompt_structure,ChatHistory,chat_completion,build_chat_history 
from utils import extract_tagged_content
from groq import Groq
from colorama import Fore
from dotenv import load_dotenv


from tool_pattern.tool import Tool ,tool, validate_args
from utils.utils import FixedChatHistory



BASE_AGENT_PROMPT = ""




REASON_AGENT_PROMPT = """
You operate by running a loop with the following steps: Thought, Action, Observation.
You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don' make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.

For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:

<tool_call>
{"name": <function-name>,"arguments": <args-dict>, "id": <monotonically-increasing-id>}
</tool_call>

Here are the available tools / actions:

<tools>
%s
</tools>

Example session:

<question>What's the current temperature in Madrid?</question>
<thought>I need to get the current weather in Madrid</thought>
<tool_call>{"name": "get_current_weather","arguments": {"location": "Madrid", "unit": "celsius"}, "id": 0}</tool_call>

You will be called again with this:

<observation>{0: {"temperature": 25, "unit": "celsius"}}</observation>

You then output:

<response>The current temperature in Madrid is 25 degrees Celsius</response>

Additional constraints:

- If the user asks you something unrelated to any of the tools above, answer freely enclosing your answer with <response></response> tags.
- If you call a tool, wait for the observation before responding.- Always use the tools. Never make up information. If you don't know, say you don't know
- Make sure the JSON is properly formatted
- Keep your responses concise and to the point
- If asked multiple questions, answer them all clearly and concisely






"""





class ReactAgent():

    def __init__(self,tools : Union[list[Tool],Tool], 
                 model : str = "llama-3.3-70b-versatile",
                 system_prompt:str=BASE_AGENT_PROMPT):
        self.model=model
        self.client=Groq()
        self.tools=tools if isinstance(tools,list) else [tools]
        self.system_prompt=system_prompt
        self.tools_dict = {tool.name: tool for tool in self.tools} if isinstance(tools,list) else {tools.name: tools}


    def add_tool_signatures_to_prompt(self,prompt : str) -> str:
        return prompt % ("".join(str(tool) for tool in self.tools))



    def process_tool_call(self,tool_calls : List[str]) -> List[str]:
        results = []
        for tool_call_str in tool_calls:
            try:
                tool_call = json.loads(tool_call_str)
            except json.JSONDecodeError as e:
                print(Fore.RED + f"Failed to parse tool call: {tool_call_str}. Error: {e}" + Fore.RESET)
                continue

            if "name" not in tool_call or "arguments" not in tool_call:
                print(Fore.RED + f"Invalid tool call format: {tool_call_str}" + Fore.RESET)
                continue

            if tool_call["name"] in self.tools_dict:
                tool = self.tools_dict[tool_call["name"]]
                try:
                    validated_args = validate_args(tool_call, json.loads(tool.func_signature))
                    result = tool.run(**validated_args)
                    results.append(f"Result from {tool_call['name']}: {result}")
                except Exception as e:
                    print(Fore.RED + f"Error executing tool {tool_call['name']}: {e}" + Fore.RESET)
        return results
    



    def run(self,query : str,max_iterations : int = 10) -> str:
        
        if self.tools:
            self.system_prompt += self.add_tool_signatures_to_prompt(REASON_AGENT_PROMPT)
        chat_history=FixedChatHistory()

        build_chat_history(chat_history,self.system_prompt,"system")
        build_chat_history(chat_history,query,"user")

        


        if self.tools :
            for iteration in range(max_iterations):
                completion=chat_completion(self.client,chat_history,self.model)

                response= extract_tagged_content(completion,"response")

                if response :
                    print(Fore.CYAN + "Final agent response:" + Fore.RESET, response[0])
                    return response[0]
                

                thoughts= extract_tagged_content(completion,"thought")
                if thoughts :
                    print(Fore.GREEN + f"Iteration {iteration+1} - Agent thought:" + Fore.RESET, thoughts[0])
                tool_calls=extract_tagged_content(completion,"tool_call")
                print(Fore.BLUE + f"Iteration {iteration+1} - Extracted tool calls:" + Fore.RESET, tool_calls)
                build_chat_history(chat_history,completion,"assistant")


                if tool_calls :
                    results= self.process_tool_call(tool_calls)
                    print(Fore.MAGENTA + f"Iteration {iteration+1} - Tool call results:" + Fore.RESET, results)
                    build_chat_history(chat_history,completion,"assistant")
                    build_chat_history(chat_history,f'observations: {results}',"user")
        
        # Get final response after all iterations or if max_iterations reached
        # Add instruction to provide final response without tool calls
        build_chat_history(chat_history, "Please provide your final response now. Do not make any more tool calls. Provide a clear, direct answer to the original query.", "user")
        final_response = chat_completion(self.client, chat_history, self.model)
        
        # Extract response if it has tags, otherwise return as is
        response_content = extract_tagged_content(final_response, "response")
        if response_content:
            final_response = response_content[0]
            
        print(Fore.CYAN + "Final agent response:" + Fore.RESET, final_response)
        return final_response
            
    

                


                



    

