from reflection_pattern.reflection_agent import ReflectionAgent


agent= ReflectionAgent()

final_response = agent.run(
    user_message="Write a Python function to calculate the factorial of a number.",
    generation_prompt="You are a Python programmer tasked with generating high quality Python code.",
    reflection_prompt="You are a Python programmer tasked with providing feedback, critique, and recommendations for the user's code.",
    n_steps=2
)

print(final_response)