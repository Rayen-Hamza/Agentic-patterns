# Agentic Patterns

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Groq-API-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/LLM-Llama%203.3%2070B-4B32C3?style=flat-square" alt="Llama"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Pattern-Multi--Agent-00C853?style=flat-square" alt="Multi-Agent"/>
  <img src="https://img.shields.io/badge/Pattern-ReAct-FF6D00?style=flat-square" alt="ReAct"/>
  <img src="https://img.shields.io/badge/Pattern-Reflection-7C4DFF?style=flat-square" alt="Reflection"/>
  <img src="https://img.shields.io/badge/Pattern-Tool%20Calling-1976D2?style=flat-square" alt="Tool"/>
</p>

A collection of AI agent design patterns implemented from scratch using Python and Groq API. Learn how to build reasoning agents, multi-agent systems, and tool-augmented LLMs.

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Patterns](#patterns)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Tests](#tests)

---

## Overview

This project implements four fundamental agentic patterns:

**Multi-Agent Pattern** - Teams of specialized agents working together with dependency management  
**ReAct Pattern** - Reasoning and acting with tool integration  
**Reflection Pattern** - Self-improvement through iterative critique  
**Tool Pattern** - Function calling with automatic schema generation  

Built with pure Python - no frameworks, just clean implementations to understand how agents work under the hood.

---

## Installation

### Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com/)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/agentic-patterns.git
cd agentic-patterns

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.exemple .env
# Add your GROQ_API_KEY to .env
```

---

## Quick Start

### Multi-Agent System

```python
from multi_agent_pattern import Agent, Crew

with Crew("Research Team") as crew:
    researcher = Agent(
        name="Researcher",
        backstory="Expert researcher",
        task_description="Research AI in healthcare",
        task_expected_output="List of 3-5 key applications"
    )
    
    writer = Agent(
        name="Writer",
        backstory="Technical writer",
        task_description="Write an article about the research",
        task_expected_output="2-3 paragraph article"
    )
    
    # Define workflow
    researcher >> writer
    
    # Execute
    results = crew.run()
```

### ReAct Agent

```python
from ReAct_pattern import ReactAgent
from tool_pattern.tool import tool

@tool
def search_web(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = ReactAgent(tools=[search_web])
response = agent.run("What is the weather in Tokyo?")
```

### Reflection Agent

```python
from reflection_pattern import ReflectionAgent

agent = ReflectionAgent()
result = agent.run(
    user_message="Write a binary search function in Python",
    generation_prompt="You are a Python expert",
    reflection_prompt="Review and critique the code",
    n_steps=3
)
```

---

## Patterns

### 1. Multi-Agent Pattern

Coordinate multiple specialized agents with automatic dependency resolution.

**Features:**
- Topological execution ordering
- Context passing between agents
- Circular dependency detection
- Workflow visualization with graphviz

**Use Cases:** Content pipelines, research workflows, complex decision systems

### 2. ReAct Pattern

Reasoning and Acting - agents think step-by-step and use tools.

**Features:**
- Explicit reasoning traces
- Dynamic tool calling
- Iterative problem solving
- Observation integration

**Use Cases:** Data analysis, API interactions, information retrieval

### 3. Reflection Pattern

Iterative improvement through generation and critique cycles.

**Features:**
- Dual-agent system (generator + reflector)
- Multiple refinement iterations
- Automatic quality checking
- Progress tracking

**Use Cases:** Code generation, content editing, error correction

### 4. Tool Pattern

Extensible function calling with automatic schema generation.

**Features:**
- `@tool` decorator for easy integration
- Auto-generated JSON schemas
- Runtime type validation
- Plug-and-play design

**Use Cases:** API wrappers, database operations, calculations

---

## Examples

### Linear Workflow

```python
with Crew("Content Creation") as crew:
    research = Agent(name="Research", ...)
    analyze = Agent(name="Analyze", ...)
    write = Agent(name="Write", ...)
    
    research >> analyze >> write
```

### Parallel Processing

```python
with Crew("Product Dev") as crew:
    market = Agent(name="Market", ...)
    tech = Agent(name="Tech", ...)
    pm = Agent(name="PM", ...)
    
    market >> pm
    tech >> pm  # Both feed into PM
```

### Tool-Augmented Agent

```python
@tool
def calculate(expr: str) -> float:
    """Evaluate math expression."""
    return eval(expr)

agent = ReactAgent(tools=[calculate])
agent.run("What is 25 * 37 + 100?")
```

---

## Project Structure

```
agentic-patterns/
├── multi_agent_pattern/      # Multi-agent orchestration
│   ├── agent.py
│   └── crew.py
├── ReAct_pattern/            # Reasoning and acting
│   └── react_agent.py
├── reflection_pattern/       # Self-improvement
│   └── reflection_agent.py
├── tool_pattern/             # Tool integration
│   ├── tool.py
│   └── tool_agent.py
├── utils/                    # Shared utilities
│   └── utils.py
└── tests/                    # Examples and tests
    ├── multi_agent_test.py
    ├── simple_multi_agent.py
    └── tool_agent.py
```

---

## Tests

Run all tests:
```bash
python -m tests.multi_agent_test
```

Run specific examples:
```bash
python -m tests.simple_multi_agent
python -m tests.tool_agent
python -m tests.reflection_agent_test
```

---

## Architecture

```
┌─────────────────────────────┐
│    Agentic Patterns         │
└──────────┬──────────────────┘
           │
    ┌──────┼──────┐
    │      │      │
┌───▼──┐ ┌─▼──┐ ┌▼────┐
│Multi │ │ReAct│ │Refl │
│Agent │ │     │ │ect  │
└──┬───┘ └──┬──┘ └─────┘
   │        │
   └────►┌──▼──┐
         │Tool │
         └─────┘
```

---

## Resources

**Research Papers:**
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Reflexion: Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

**Related Projects:**
- [LangChain](https://github.com/langchain-ai/langchain)
- [CrewAI](https://github.com/joaomdmoura/crewAI)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">Made with Python & Groq</p>

