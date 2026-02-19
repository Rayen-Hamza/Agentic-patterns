from dotenv import load_dotenv
from tool_pattern.tool import tool
from tool_pattern.tool_agent import ToolAgent,TOOL_AGENT_PROMPT
from groq import Groq 
from utils.utils import build_prompt_structure,FixedChatHistory,chat_completion,build_chat_history

from ReAct_pattern.react_agent import ReactAgent
load_dotenv()


@tool
def get_weather_data(location: str, date: str) -> dict:
    """
    Fetch weather data for a specific location and date.
    """
    # Dummy implementation for illustration
    return {
        "location": location,
        "date": date,
        "temperature": "22°C",
        "condition": "Sunny"
    }

@tool
def get_population_data(city: str) -> dict:
    """
    Fetch population data for a specific city.
    """
    # Dummy implementation for illustration
    population_data = {
        "New York": {"population": "8.4 million", "density": "10,716 people per sq km"},
        "Tokyo": {"population": "13.9 million", "density": "6,158 people per sq km"},
        "London": {"population": "9.0 million", "density": "5,701 people per sq km"},
        "Paris": {"population": "2.2 million", "density": "20,781 people per sq km"},
    }
    
    return {
        "city": city,
        "data": population_data.get(city, {"population": "unknown", "density": "unknown"})
    }


tool_agent = ReactAgent(tools=[get_weather_data, get_population_data])
tool_agent.run("what is the weather in New York on 2023-10-10 and what is the population of Tokyo?")



























