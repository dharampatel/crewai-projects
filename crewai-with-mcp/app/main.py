import streamlit as st
from crewai import Crew, Process
from app.agents import math_expert, story_expert, classify_query_type
import asyncio

from app.tasks import create_math_task, create_story_task

async def run_crew_async(crew: Crew):
    return crew.kickoff()

st.set_page_config(page_title="CrewAI Assistant", page_icon="🧠")
st.title("🧠 CrewAI Assistant")
st.markdown("Ask a **math question** or request a **story**. The Manager will assign the right expert.")

question = st.text_input("Enter your query:", placeholder="e.g., What is 18 * 25? or Write a story about a time traveler.")

if st.button("Run Task"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Manager analyzing and assigning task..."):
            query_type = classify_query_type(question)

            if query_type == "math":
                task = create_math_task(question)
                agents = [math_expert]
            elif query_type == "story":
                task = create_story_task(question)
                agents = [story_expert]
            else:
                st.error("Unable to classify your query. Try again.")
                st.stop()

            crew = Crew(
                agents=agents,
                tasks=[task],
                process=Process.sequential,
                verbose=True,
            )

            # Run the crew
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_crew_async(crew))

        st.success("✅ Task Completed!")
        st.markdown("### ✨ Result:")
        for task in result.tasks_output:
            st.write(f"Task by {task.agent}")
            st.markdown(task.raw)

        with st.expander("🔍 Debug Info"):
            st.write(f"**Query Type**: `{query_type}`")
            st.write(f"**Agents Used**: {[agent.role for agent in agents]}")
            st.write(f"**Task Description**: {task.description}")
