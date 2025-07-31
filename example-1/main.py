from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()


# Create LLM Object
llm = LLM(model='gemini/gemini-2.0-flash',api_key=os.getenv("GOOGLE_API_KEY"))

# Step-1: create tool
tavily_tool = TavilySearchResults(k=1, tavily_api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search_tool(query: str):
  """Search the web for information on a given topic"""
  return tavily_tool.invoke(query)

# Step-2: Create Agent
searcher = Agent(
    role='Content Researcher',
    goal='Research and collect online content about {topic}',
    backstory='''
        You are responsible for conducting thorough online research related to {topic}. 
        Your task is to find and group relevant, credible, and up-to-date information, including recent trends, key figures, and news. 
        Your findings will be used by the Content Writer to create a high-quality LinkedIn article.
    ''',
    tools=[web_search_tool],
    llm=llm,
    verbose=True,
    allow_delegate=False
)

writer = Agent(
    role='Content Writer',
    goal='Craft an engaging LinkedIn article about {topic}',
    backstory='''
        Based on the research provided by the Content Researcher, your task is to write an informative and engaging LinkedIn post on {topic}. 
        The article should be well-structured, insightful, and optimized with relevant SEO keywords to attract and inform the intended audience.
    ''',
    tools=[web_search_tool],
    llm=llm,
    verbose=True
)

editor = Agent(
    role='Content Editor',
    goal='Edit the LinkedIn article for clarity, tone, and factual accuracy',
    backstory='''
        You are tasked with reviewing the LinkedIn article created by the Content Writer. 
        Your goal is to ensure it is free from grammatical errors, factually accurate, and written in a professional yet approachable tone.
        The final article should be publication-ready and formatted cleanly into paragraphs without bullet points.
    ''',
    tools=[web_search_tool],
    llm=llm,
    verbose=True
)

# Step-3: Create Tasks
search = Task(
    description='''
        1. Conduct online research to gather recent insights, data, trends, and news about {topic}.
        2. Identify the target audience, understanding their interests, challenges, and professional context.
        3. Collect relevant SEO keywords and cite data from trustworthy, authoritative sources.
    ''',
    agent=searcher,
    expected_output='A detailed research brief on {topic}, highlighting key trends, SEO keywords, target audience insights, and recent developments.'
)

write = Task(
    description='''
        1. Use the research findings to draft a compelling, well-structured LinkedIn article focused on {topic}.
        2. Integrate relevant SEO keywords naturally throughout the content.
        3. Ensure the tone is engaging and informative, ending with a thoughtful conclusion to prompt audience reflection or interaction.
    ''',
    agent=writer,
    expected_output='A professionally written LinkedIn article on {topic}, optimized for SEO and tailored for the intended audience.'
)

review = Task(
    description='''
        Carefully review the draft article for:
        - Grammatical correctness and fluency
        - Factual accuracy and clarity
        - Engaging tone and readability
        Final output should be a cleanly formatted LinkedIn article in paragraphs, free of bullet points and ready for immediate publication.
    ''',
    agent=editor,
    expected_output='A polished LinkedIn article about {topic}, edited for tone, style, grammar, and factual accuracy.'
)

# Step-4: Crate crew and finalize process
crew = Crew(
    agents=[searcher,writer,editor],
    tasks=[search,write,review],
    process=Process.sequential
)

subject = 'Career opportunities for developers specializing in Multi-Agent Systems'

template_input = {"topic": subject}

result = crew.kickoff(inputs=template_input)



