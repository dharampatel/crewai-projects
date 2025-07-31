from crewai import Agent, LLM

from app.tools import get_tools
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()


# Create LLM Object
llm = LLM(model='gemini/gemini-2.0-flash',api_key=os.getenv("GOOGLE_API_KEY"))

tools = get_tools()
math_tools = [t for t in tools if t.name in {"add", "multiply", "calculate_bmi"}]
story_tools = [t for t in tools if t.name == "write_story"]

manager = Agent(
    role="Manager",
    goal="Analyze user query and delegate it to the correct agent (math or story).",
    backstory="""
    You're a manager responsible for classifying whether a user question is a math problem or a creative writing request.
    Based on the classification, you should assign the task to the appropriate expert.
    """,
    llm=llm
)

math_expert = Agent(
    role='Math Expert',
    goal='Solve math problems by. using tools',
    backstory='''
        You are responsible for solving math problems. 
        Your task to find the correct tools to solve the math problems.
    ''',
    tools=math_tools,
    llm=llm,
    verbose=True,
    allow_delegate=False
)

story_expert = Agent(
    role='Story Writer',
    goal='Craft an engaging Story',
    backstory='''
        Your task is to write an informative and engaging Story. 
        The story should be well-structured, insightful, and optimized to attract and inform the intended audience.
    ''',
    tools=story_tools,
    llm=llm,
    verbose=True
)


def classify_query_type(query: str):
    template = PromptTemplate.from_template("""
    You are a classification assistant.
    Classify the following query as either 'math' or 'story':
    "{query}"
    Your answer should be only one word: 'math' or 'story'.
    """)
    response = manager.llm.call(template.format(query=query)).strip().lower()
    return response
