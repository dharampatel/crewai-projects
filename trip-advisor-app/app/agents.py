from crewai import Agent, LLM
import os
from dotenv import load_dotenv

from app.tools import web_search_tool

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

guide_expert = Agent(
    role="City Local Guide Expert",
    goal="Provides information on things to do in the city based on user interests.",
    backstory="A local expert passionate about sharing city experiences.",
    tools=[web_search_tool],
    verbose=True,
    max_iter=5,
    allow_delegation=False,
    llm=llm
)

location_expert = Agent(
    role="Travel Trip Expert",
    goal="Provides travel logistics and essential information.",
    backstory="A seasoned traveler who knows everything about different cities.",
    tools=[web_search_tool],
    verbose=True,
    max_iter=5,
    allow_delegation=False,
    llm=llm
)

planning_expert = Agent(
    role="Travel Planning Expert",
    goal="Compiles all gathered information to create a travel plan.",
    backstory="An expert in planning seamless travel itineraries.",
    tools=[web_search_tool],
    verbose=True,
    max_iter=5,
    allow_delegation=False,
    llm=llm
)