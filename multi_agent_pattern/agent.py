from textwrap import dedent
from .crew import Crew
from ReAct_pattern import ReactAgent 
from tool_pattern.tool import Tool 



class Agent:
    """
    An autonomous agent that can work independently or as part of a multi-agent crew.
    
    Agents can have dependencies on other agents, forming a directed graph where
    dependencies are executed first. Each agent uses a ReAct pattern internally
    to process tasks with optional tool usage.
    
    Attributes:
        name: Unique identifier for the agent
        backstory: Agent's role description and personality
        task_description: The specific task this agent should complete
        task_expected_output: Format specification for the agent's output
        react_agent: Internal ReAct agent for task execution
        dependencies: List of agents this agent depends on (runs after them)
        dependents: List of agents that depend on this agent (run after this)
        context: Accumulated context from dependency agents
    """
    
    def __init__(
            self,
            name: str,
            backstory: str,
            task_description: str,
            task_expected_output: str,
            tools: list[Tool] | None = None,
            llm: str = "llama-3.3-70b-versatile"

    ):
        """
        Initialize an Agent.
        
        Args:
            name: Unique identifier for the agent
            backstory: Description of the agent's role and expertise
            task_description: The task this agent should complete
            task_expected_output: Expected format/content of the output
            tools: Optional list of tools the agent can use
            llm: LLM model to use (default: llama-3.3-70b-versatile)
        """
        self.name = name
        self.backstory = backstory
        self.task_description = task_description
        self.task_expected_output = task_expected_output
        self.react_agent = ReactAgent(tools=tools or [], model=llm , system_prompt= self.backstory)
        self.dependencies : list[Agent] = []
        self.dependents : list[Agent] = []

        self.context=""
        
        # Auto-register with active crew if within context manager
        try:
            Crew.register_agent(self)
        except RuntimeError:
            # No active crew - agent created outside context manager
            pass



    def __lshift__(self, other):
        """Left shift operator: self << other makes other dependent on self."""
        self.add_dependent(other)
        return other

    def __rshift__(self, other):
        """Right shift operator: self >> other makes self dependent on other."""
        self.add_dependency(other)
        return other
    
    def __rrshift__(self, other):
        """Reflected right shift: other >> self when other doesn't support >>."""
        self.add_dependency(other)
        return self
    
    def __rlshift__(self, other):
        """Reflected left shift: other << self when other doesn't support <<."""
        self.add_dependent(other)
        return self


    def add_dependency(self, agent):
        """
        Add a dependency agent that must execute before this agent.
        
        Args:
            agent: Agent or list of Agents to depend on
            
        Raises:
            TypeError: If agent is not an Agent instance or list of Agents
        """
        if isinstance(agent, Agent):
            if agent not in self.dependencies:
                self.dependencies.append(agent)
                agent.dependents.append(self)

        elif isinstance(agent, list) and all(isinstance(a, Agent) for a in agent):
            for a in agent:
                if a not in self.dependencies:
                    self.dependencies.append(a)
                    a.dependents.append(self)
        else:
            raise TypeError("Dependency must be an Agent instance or a list of Agent instances.")
        

    def add_dependent(self, agent):
        """
        Add a dependent agent that will execute after this agent.
        
        Args:
            agent: Agent or list of Agents that depend on this agent
            
        Raises:
            TypeError: If agent is not an Agent instance or list of Agents
        """
        if isinstance(agent, Agent):
            if agent not in self.dependents:
                self.dependents.append(agent)
                agent.dependencies.append(self)

        elif isinstance(agent, list) and all(isinstance(a, Agent) for a in agent):
            for a in agent:
                if a not in self.dependents:
                    self.dependents.append(a)
                    a.dependencies.append(self)
        else:
            raise TypeError("Dependent must be an Agent instance or a list of Agent instances.")



    def receive_context(self, context: str):
        """
        Receive and accumulate context from another agent.
        
        Args:
            context: Context string from a dependency agent
        """
        self.context += f" {self.name} received context: {context}."
    
    def clear_context(self):
        """Clear accumulated context for this agent."""
        self.context = ""
    
    def __repr__(self):
        return f"Agent(name='{self.name}', dependencies={len(self.dependencies)}, dependents={len(self.dependents)})"
    
    def create_prompt(self):
        """
        Create a structured prompt for the agent's LLM.
        
        Returns:
            str: Formatted prompt including task, context, and instructions
        """
        prompt = dedent(f"""
        You are {self.name}, an AI agent working collaboratively within a multi-agent system.
        
        ## Your Role & Backstory
        {self.backstory}
        
        ## Task Assignment
        Complete the following task with precision and attention to detail:
        
        <task_description>
        {self.task_description}
        </task_description>
        
        ## Expected Output Format
        Your response MUST adhere to the following format specifications:
        
        <task_expected_output>
        {self.task_expected_output}
        </task_expected_output>
        
        ## Team Collaboration
        - **Dependencies (agents you rely on)**: {', '.join([dep.name for dep in self.dependencies]) if self.dependencies else 'None'}
        - **Dependents (agents relying on you)**: {', '.join([dep.name for dep in self.dependents]) if self.dependents else 'None'}
        
        ## Available Context
        Use the context below from other agents to inform your response. If empty, proceed with the information available:
        
        <context>
        {self.context if self.context else 'No context available yet.'}
        </context>
        
        ## Instructions
        1. Analyze the task description and any provided context carefully
        2. Generate a response that fulfills the task requirements
        3. Format your output exactly as specified in the expected output section
        4. Ensure your work integrates smoothly with dependent agents' needs
        5. If the expected output format is not specified, create a clear and comprehensive response
        
        Now, complete your assigned task.
        """
        ).strip()
        return prompt


    def execute(self):
        """
        Execute the agent's task using the ReAct pattern.
        
        Passes the generated response to all dependent agents as context.
        
        Returns:
            str: The agent's response after completing its task
        """
        prompt = self.create_prompt()
        response = self.react_agent.run(prompt)
        for dependent in self.dependents:
            dependent.receive_context(response)
        
        return response
