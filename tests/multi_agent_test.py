"""
Test suite for multi-agent pattern.

This module demonstrates and tests the functionality of the multi-agent system,
including agent creation, dependency management, crew orchestration, and execution.
"""
from dotenv import load_dotenv

# Import from multi_agent_pattern (now with underscore)
from multi_agent_pattern.agent import Agent
from multi_agent_pattern.crew import Crew
from tool_pattern.tool import tool

load_dotenv()


# Example 1: Simple linear dependency chain
def test_linear_dependency():
    """
    Test a simple linear dependency chain: A -> B -> C
    Each agent depends on the previous one.
    """
    print("\n" + "="*60)
    print("TEST 1: Linear Dependency Chain")
    print("="*60)
    
    with Crew("Linear Research Team") as crew:
        # Agent A: Research
        researcher = Agent(
            name="Researcher",
            backstory="You are an expert researcher who gathers information on topics.",
            task_description="Research the benefits of artificial intelligence in healthcare.",
            task_expected_output="A brief summary of 3-5 key benefits in bullet points."
        )
        
        # Agent B: Analyzer (depends on Researcher)
        analyzer = Agent(
            name="Analyzer",
            backstory="You are a data analyst who examines research findings.",
            task_description="Analyze the research findings and identify the most impactful benefit.",
            task_expected_output="A single paragraph identifying the most significant benefit and why."
        )
        
        # Agent C: Writer (depends on Analyzer)
        writer = Agent(
            name="Writer",
            backstory="You are a content writer who creates engaging content.",
            task_description="Write a compelling introduction paragraph for a blog post about AI in healthcare.",
            task_expected_output="An engaging 3-4 sentence introduction paragraph."
        )
        
        # Set up dependencies: Researcher -> Analyzer -> Writer
        researcher >> analyzer >> writer
        
        # Execute the crew
        print(f"\nCrew: {crew}")
        print(f"Agents: {[agent.name for agent in crew.agents]}")
        
        results = crew.run()
        
        print("\n" + "-"*60)
        print("Results:")
        print("-"*60)
        for agent_name, result in results.items():
            print(f"\n{agent_name}:\n{result}\n")


# Example 2: Parallel dependencies (fan-in pattern)
def test_parallel_dependencies():
    """
    Test parallel dependencies where multiple agents feed into one:
    A -> C
    B -> C
    """
    print("\n" + "="*60)
    print("TEST 2: Parallel Dependencies (Fan-in)")
    print("="*60)
    
    with Crew("Product Development Team") as crew:
        # Agent A: Market Research
        market_researcher = Agent(
            name="MarketResearcher",
            backstory="You are a market research expert.",
            task_description="Identify current market trends for mobile apps.",
            task_expected_output="List 3 current market trends."
        )
        
        # Agent B: Tech Research
        tech_researcher = Agent(
            name="TechResearcher",
            backstory="You are a technology trends expert.",
            task_description="Identify emerging technologies for mobile development.",
            task_expected_output="List 3 emerging technologies."
        )
        
        # Agent C: Product Manager (depends on both researchers)
        product_manager = Agent(
            name="ProductManager",
            backstory="You are a product manager who synthesizes research into product ideas.",
            task_description="Based on market and tech research, propose a mobile app concept.",
            task_expected_output="A one-paragraph app concept description."
        )
        
        # Set up parallel dependencies
        market_researcher >> product_manager
        tech_researcher >> product_manager
        
        # Execute
        print(f"\nCrew: {crew}")
        results = crew.run()
        
        print("\n" + "-"*60)
        print("Results:")
        print("-"*60)
        for agent_name, result in results.items():
            print(f"\n{agent_name}:\n{result}\n")


# Example 3: Complex dependency graph
def test_complex_dependencies():
    """
    Test a complex dependency graph:
    A -> C -> E
    B -> D -> E
    """
    print("\n" + "="*60)
    print("TEST 3: Complex Dependency Graph")
    print("="*60)
    
    with Crew("Content Creation Pipeline") as crew:
        # Level 1: Two independent researchers
        topic_researcher = Agent(
            name="TopicResearcher",
            backstory="You research trending topics.",
            task_description="Find a trending topic in technology.",
            task_expected_output="One trending technology topic."
        )
        
        audience_researcher = Agent(
            name="AudienceResearcher",
            backstory="You analyze target audiences.",
            task_description="Identify the target audience for tech content.",
            task_expected_output="Description of target audience demographics."
        )
        
        # Level 2: Two agents processing the research
        content_strategist = Agent(
            name="ContentStrategist",
            backstory="You create content strategies based on topics.",
            task_description="Develop a content strategy for the topic.",
            task_expected_output="A brief content strategy outline."
        )
        
        tone_specialist = Agent(
            name="ToneSpecialist",
            backstory="You define appropriate tone based on audience.",
            task_description="Define the tone for content targeting this audience.",
            task_expected_output="Description of appropriate tone."
        )
        
        # Level 3: Final writer combining all inputs
        content_writer = Agent(
            name="ContentWriter",
            backstory="You write content based on strategy, tone, and topic.",
            task_description="Write a short article incorporating all guidance.",
            task_expected_output="A 2-paragraph article."
        )
        
        # Set up complex dependencies
        topic_researcher >> content_strategist >> content_writer
        audience_researcher >> tone_specialist >> content_writer
        
        print(f"\nCrew: {crew}")
        print("\nDependency visualization:")
        for agent in crew.agents:
            deps = [d.name for d in agent.dependencies]
            print(f"  {agent.name} depends on: {deps if deps else 'None'}")
        
        results = crew.run()
        
        print("\n" + "-"*60)
        print("Results:")
        print("-"*60)
        for agent_name, result in results.items():
            print(f"\n{agent_name}:\n{result}\n")


# Example 4: Testing with tools
def test_agents_with_tools():
    """
    Test agents using tools for enhanced capabilities.
    """
    print("\n" + "="*60)
    print("TEST 4: Agents with Tools")
    print("="*60)
    
    # Define some example tools
    @tool
    def search_database(query: str) -> str:
        """Search a database for information."""
        # Mock implementation
        return f"Database results for '{query}': Found 5 relevant entries about {query}."
    
    @tool
    def calculate_metrics(data: str) -> str:
        """Calculate metrics from data."""
        # Mock implementation
        return "Metrics: Average=75, Median=78, StdDev=12"
    
    with Crew("Data Analysis Team") as crew:
        # Data collector with tools
        collector = Agent(
            name="DataCollector",
            backstory="You collect data using available tools.",
            task_description="Collect information about user engagement.",
            task_expected_output="Summary of collected data.",
            tools=[search_database]
        )
        
        # Analyst with tools
        analyst = Agent(
            name="DataAnalyst",
            backstory="You analyze data and calculate metrics.",
            task_description="Analyze the collected data and provide metrics.",
            task_expected_output="Statistical analysis summary.",
            tools=[calculate_metrics]
        )
        
        # Report writer
        reporter = Agent(
            name="Reporter",
            backstory="You write clear reports based on analysis.",
            task_description="Create a summary report of the findings.",
            task_expected_output="A concise report paragraph."
        )
        
        # Set up pipeline
        collector >> analyst >> reporter
        
        print(f"\nCrew: {crew}")
        results = crew.run()
        
        print("\n" + "-"*60)
        print("Results:")
        print("-"*60)
        for agent_name, result in results.items():
            print(f"\n{agent_name}:\n{result}\n")


# Example 5: Testing circular dependency detection
def test_circular_dependency_detection():
    """
    Test that circular dependencies are properly detected and raise an error.
    """
    print("\n" + "="*60)
    print("TEST 5: Circular Dependency Detection")
    print("="*60)
    
    try:
        with Crew("Circular Test") as crew:
            agent_a = Agent(
                name="AgentA",
                backstory="Agent A",
                task_description="Task A",
                task_expected_output="Output A"
            )
            
            agent_b = Agent(
                name="AgentB",
                backstory="Agent B",
                task_description="Task B",
                task_expected_output="Output B"
            )
            
            agent_c = Agent(
                name="AgentC",
                backstory="Agent C",
                task_description="Task C",
                task_expected_output="Output C"
            )
            
            # Create circular dependency: A -> B -> C -> A
            agent_a >> agent_b >> agent_c >> agent_a
            
            print("Attempting to run crew with circular dependencies...")
            crew.run()
            
            print("ERROR: Circular dependency was not detected!")
            
    except ValueError as e:
        print(f"✓ Successfully detected circular dependency: {e}")


# Example 6: Testing operator overloading
def test_operator_overloading():
    """
    Test the << and >> operators for dependency setup.
    """
    print("\n" + "="*60)
    print("TEST 6: Operator Overloading")
    print("="*60)
    
    with Crew("Operator Test") as crew:
        agent1 = Agent(
            name="Agent1",
            backstory="First agent",
            task_description="Do task 1",
            task_expected_output="Output 1"
        )
        
        agent2 = Agent(
            name="Agent2",
            backstory="Second agent",
            task_description="Do task 2",
            task_expected_output="Output 2"
        )
        
        agent3 = Agent(
            name="Agent3",
            backstory="Third agent",
            task_description="Do task 3",
            task_expected_output="Output 3"
        )
        
        # Test >> operator (right shift)
        agent1 >> agent2
        
        # Test << operator (left shift)
        agent2 << agent3
        
        print("\nDependency setup:")
        print(f"  Agent1 dependencies: {[a.name for a in agent1.dependencies]}")
        print(f"  Agent2 dependencies: {[a.name for a in agent2.dependencies]}")
        print(f"  Agent3 dependencies: {[a.name for a in agent3.dependencies]}")
        print(f"  Agent2 dependents: {[a.name for a in agent2.dependents]}")
        
        # Verify
        assert agent2 in agent1.dependents, "Agent2 should be dependent on Agent1"
        assert agent1 in agent2.dependencies, "Agent1 should be a dependency of Agent2"
        assert agent3 in agent2.dependents, "Agent3 should be dependent on Agent2"
        assert agent2 in agent3.dependencies, "Agent2 should be a dependency of Agent3"
        
        print("\n✓ All operator tests passed!")


# Example 7: Testing crew visualization
def test_crew_visualization():
    """
    Test the plot functionality for visualizing agent dependencies.
    """
    print("\n" + "="*60)
    print("TEST 7: Crew Visualization")
    print("="*60)
    
    with Crew("Visualization Test") as crew:
        a = Agent(name="Start", backstory="Starting point", 
                 task_description="Begin", task_expected_output="Begin output")
        b = Agent(name="Process1", backstory="First processor",
                 task_description="Process 1", task_expected_output="Process 1 output")
        c = Agent(name="Process2", backstory="Second processor",
                 task_description="Process 2", task_expected_output="Process 2 output")
        d = Agent(name="End", backstory="Final step",
                 task_description="Finalize", task_expected_output="Final output")
        
        # Create dependencies
        a >> b >> d
        a >> c >> d
        
        # Generate graph (but don't view it automatically)
        graph = crew.plot(filename=None, view=False)
        
        print(f"✓ Generated graph with {len(crew.agents)} agents")
        print(f"  Graph format: {graph.format}")
        print(f"  To visualize, call: crew.plot(filename='my_crew', view=True)")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*60)
    print("MULTI-AGENT PATTERN TEST SUITE")
    print("="*60)
    
    # Run tests
    test_linear_dependency()
    test_parallel_dependencies()
    test_complex_dependencies()
    test_agents_with_tools()
    test_circular_dependency_detection()
    test_operator_overloading()
    test_crew_visualization()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    # Run individual tests
    # test_linear_dependency()
    # test_parallel_dependencies()
    # test_complex_dependencies()
    # test_agents_with_tools()
    # test_circular_dependency_detection()
    # test_operator_overloading()
    # test_crew_visualization()
    
    # Or run all tests
    run_all_tests()
