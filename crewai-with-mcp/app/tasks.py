from crewai import Task

from app.agents import math_expert, story_expert


def create_math_task(question: str):
    return Task(
        description=f'''
            Solve the following math problem: "{question}".
            Use appropriate tools like addition, multiplication, or BMI calculator.
            Explain step-by-step reasoning and provide the final answer.
        ''',
        agent=math_expert,
        expected_output='Step-by-step explanation and final answer to the math problem.'
    )

def create_story_task(question: str):
    return Task(
        description=f'''
            Write an engaging story based on: "{question}".
            Ensure the story has a clear beginning, middle, and end.
            Make it interesting, thoughtful, and emotionally resonant.
        ''',
        agent=story_expert,
        expected_output='A creative, well-structured story based on the input prompt.'
    )