

from dotenv import load_dotenv
from tool_pattern.tool import tool
from tool_pattern.tool_agent import ToolAgent,TOOL_AGENT_PROMPT



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



tool_agent = ToolAgent(tools=[get_weather_data])

print(tool_agent.add_tool_signatures_to_prompt(TOOL_AGENT_PROMPT))
















