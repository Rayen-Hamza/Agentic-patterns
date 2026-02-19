from colorama import Fore
from graphviz import Digraph



class Crew:
    """
    A crew manages a collection of agents and orchestrates their execution.
    
    Crews use a context manager pattern to automatically register agents and
    execute them in topological order based on their dependencies.
    
    Attributes:
        name: Name identifier for the crew
        agents: List of agents in this crew
        current_crew: Class variable tracking the active crew context
    
    Example:
        >>> with Crew("Research Team") as crew:
        ...     researcher = Agent(name="Researcher", ...)
        ...     writer = Agent(name="Writer", ...)
        ...     researcher >> writer  # Writer depends on Researcher
        ...     results = crew.run()
    """
    
    current_crew = None

    def __init__(self, name: str):
        """
        Initialize a Crew.
        
        Args:
            name: Identifier for this crew
        """
        self.name = name
        self.agents = []

    def __enter__(self):
        """Enter the crew context. Agents created within will auto-register."""
        Crew.current_crew = self
        return self
    


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the crew context and clear the current crew."""
        Crew.current_crew = None
        return False  

    def __repr__(self):
        return f"Crew(name='{self.name}', agents={len(self.agents)})"

    def add_agent(self, agent):
        """
        Add an agent to this crew.
        
        Args:
            agent: Agent instance to add
        """
        self.agents.append(agent)

    @staticmethod
    def register_agent(agent):
        """
        Register an agent with the currently active crew.
        
        Called automatically when an agent is created within a crew context.
        
        Args:
            agent: Agent instance to register
            
        Raises:
            RuntimeError: If no crew context is active
        """
        if Crew.current_crew is not None:
            Crew.current_crew.add_agent(agent)
        else:
            raise RuntimeError("No active crew to register the agent to.")
        

    def plot(self, filename=None, view=False):
        """
        Create a visual graph of agent dependencies.
        
        Args:
            filename: If provided, saves the graph to this file (without extension)
            view: If True, opens the graph automatically
        
        Returns:
            Digraph object
        """
        dot = Digraph(comment=self.name)
        dot.attr(rankdir='LR')  # Left to right layout
        
        for agent in self.agents:
            dot.node(agent.name, agent.name, shape='box', style='rounded,filled', fillcolor='lightblue')
            for dep in agent.dependencies:
                dot.edge(dep.name, agent.name, label='depends on')
        
        if filename:
            dot.render(filename, view=view, cleanup=True)
        elif view:
            dot.render('temp_crew_graph', view=True, cleanup=True)
            
        return dot
    
    
    def topological_sort(self):
        """
        Sort agents in topological order based on dependencies.
        
        Ensures that agents are executed in an order where all dependencies
        complete before their dependents run.
        
        Returns:
            list[Agent]: Agents sorted in execution order
            
        Raises:
            ValueError: If circular dependencies are detected
        """
        visited = set()
        in_progress = set()
        sorted_agents = []

        def visit(agent):
            if agent in visited:
                return
            if agent in in_progress:
                raise ValueError(f"Circular dependency detected involving agent: {agent.name}")
            
            in_progress.add(agent)
            for dep in agent.dependencies:
                visit(dep)
            in_progress.remove(agent)
            visited.add(agent)
            sorted_agents.append(agent)

        for agent in self.agents:
            visit(agent)

        return sorted_agents

    def run(self):
        """
        Execute all agents in the crew in topological order.
        
        Each agent executes and passes its output as context to dependent agents.
        
        Returns:
            dict: Mapping of agent names to their execution results
        """
        sorted_agents = self.topological_sort()
        results = {}
        for agent in sorted_agents:
            print(f"{Fore.GREEN}Running agent: {agent.name}{Fore.RESET}")
            results[agent.name] = agent.execute()
        return results

    
