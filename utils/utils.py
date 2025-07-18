def chat_completion(client, chat_history, model="llama-3.3-70b-versatile")-> str:
    """
    Function to get chat completion from the Groq client.
    
    Args:
        client: The Groq client instance.
        chat_history: List of messages in the chat history.
        model: The model to use for the chat completion.
        
    Returns:
        The content of the response message.
    """
    response = client.chat.completions.create(
        model=model,
        messages=chat_history,
    )
    return str(response.choices[0].message.content)



def build_prompt_structure(prompt : str , role :str,tag :str = " ") -> dict :
    """
    Function to build the chat prompt structure.
    
    Args:
        system_prompt: The system prompt to be used.
        user_message: The user's message.
        
    Returns:
        A list containing the system prompt and the user message.
    """
    if tag :
        prompt = f"<{tag}> {prompt} </{tag}>" 

    return {"role": role, "content": prompt}



def build_chat_history(history :list , prompt : str, role :str ):
    """
    Function to build the chat history for the Groq client.
    
    Args:
        system_prompt: The system prompt to be used.
        user_message: The user's message.
        tag: Optional tag to wrap the user message.
        
    Returns:
        A list containing the system prompt and the user message.
  
    """

    history.append(build_prompt_structure(prompt, role))





class ChatHistory(list):
    def __init__(self,messages=None,total_length=0):
        """
        Initialize the chat history with an optional list of messages.
        
        Args:
            messages: Optional initial messages to populate the chat history.
        """
        super().__init__(messages if messages is not None else [])
        self.total_length=total_length




    def append(self, msg):
        if len(self) >= self.total_length:
            self.pop(0)

        super().append(msg)



       

class FixedChatHistory(ChatHistory):
    def __init__(self, messages=None, total_length=5):
        super().__init__(messages, total_length)



    def append(self, msg):
        if len(self) >= self.total_length:
            self.pop(1) # Remove the second message to keep the system prompt intact 
        super().append(msg)
