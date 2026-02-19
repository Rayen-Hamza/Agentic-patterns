"""
Simple example demonstrating the multi-agent pattern.

This example shows how to create a basic multi-agent workflow where
multiple agents collaborate to complete a task.
"""

from dotenv import load_dotenv
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from multi_agent_pattern (renamed from multi-agent-pattern)
from multi_agent_pattern.agent import Agent
from multi_agent_pattern.crew import Crew

load_dotenv()


def simple_example():
    """
    Simple example: Research -> Analyze -> Write
    
    Three agents work together to research a topic, analyze findings,
    and write a summary.
    """
    print("="*60)
    print("Simple Multi-Agent Example")
    print("="*60)
    
    # Create a crew with context manager
    with Crew("Content Creation Team") as crew:
        
        # Agent 1: Researcher
        researcher = Agent(
            name="Researcher",
            backstory="You are an expert researcher who gathers comprehensive information.",
            task_description="Research the main benefits of using microservices architecture.",
            task_expected_output="A list of 3-4 key benefits in bullet point format."
        )
        
        # Agent 2: Analyzer  
        analyzer = Agent(
            name="Analyzer",
            backstory="You are a technical analyst who evaluates information critically.",
            task_description="Analyze the benefits provided and identify any trade-offs or challenges.",
            task_expected_output="A brief analysis highlighting one key challenge for each benefit."
        )
        
        # Agent 3: Writer
        writer = Agent(
            name="Writer",
            backstory="You are a technical writer who creates clear, engaging content.",
            task_description="Write a concise article summarizing the benefits and challenges of microservices.",
            task_expected_output="A well-structured article with 2-3 paragraphs."
        )
        
        # Set up the workflow: Researcher -> Analyzer -> Writer
        researcher >> analyzer >> writer
        
        print(f"\nCrew created: {crew}")
        print(f"Number of agents: {len(crew.agents)}")
        print("\nAgent dependencies:")
        for agent in crew.agents:
            deps = [d.name for d in agent.dependencies]
            print(f"  {agent.name}: depends on {deps if deps else 'none'}")
        
        # Execute the workflow
        print("\n" + "-"*60)
        print("Executing agents...")
        print("-"*60 + "\n")
        
        results = crew.run()
        
        # Display results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        
        for agent_name, result in results.items():
            print(f"\n{agent_name}:")
            print("-" * 40)
            print(result)
            print()


if __name__ == "__main__":
    simple_example()
