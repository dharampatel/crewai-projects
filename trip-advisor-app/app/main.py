import streamlit as st
from crewai import Crew, Process

from app.agents import location_expert, guide_expert, planning_expert
from app.tasks import location_task, guide_task, planner_task

st.title("🌍 AI-Powered Trip Advisor")

st.markdown("""
    **Plan your next trip with Trip Advisor!**  
    Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary including:
     1. Best places to visit 
     2. Accommodation & budget planning 
     3. Local food recommendations   
     4. Transportation & visa details
    """
)

# User input
from_city = st.text_input("(From)Enter city or country name", "India")
des_city = st.text_input("(Destination)Enter city or country name", "London")
from_date = st.date_input("Departure Date")
to_date = st.date_input("Return Date")
interests = st.text_area("Your Interests (e.g., sightseeing, food, adventure)", "sightseeing and good food")

if st.button("Generate Trip Plan"):
    if not from_city or not des_city or not from_date or not to_date or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        with st.spinner("Trip Assistant is preparing your travel plan... Please wait..."):

            # Initialize Tasks
            loc_task = location_task(location_expert, from_city, des_city, from_date, to_date)
            guid_task = guide_task(guide_expert, des_city, interests, from_date, to_date)
            plan_task = planner_task([loc_task, guid_task], planning_expert, des_city, interests, from_date, to_date)

            # setup crew
            crew = Crew(
                agents=[location_expert, guide_expert, planning_expert],
                tasks=[loc_task, guid_task, plan_task],
                process=Process.sequential,
                verbose=True,
            )

            result = crew.kickoff()

            # Show Results
            st.subheader("Your Travel Plan")
            st.markdown(result)

            # Ensure result is a string
            travel_plan_text = str(result)

            st.download_button(
                label="Download Travel Plan",
                data=travel_plan_text,
                file_name=f"Travel_Plan_{des_city}.txt",
                mime="text/plain"
            )