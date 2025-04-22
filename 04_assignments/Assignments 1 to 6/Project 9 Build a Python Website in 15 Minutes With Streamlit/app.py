import streamlit as st
from dotenv import load_dotenv
import os
import requests
import random
import time
import json

# Load environment variables from .env file
load_dotenv()

# Custom CSS with enhanced styles (your styling preserved)
st.markdown("""...<YOUR CSS CONTENT HERE>...""", unsafe_allow_html=True)

# Hugging face API setup
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Example model
headers = {"Authorization": f"Bearer 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"}

# Function to query Hugging Face API
def query_huggingface(payload):
    try:
        if isinstance(payload, dict):
            text = payload.get('inputs', '')
        else:
            text = str(payload)

        simple_payload = {
            'inputs': text,
            'options': {"wait_for_model": True}
        }

        response = requests.post(API_URL, headers=headers, json=simple_payload)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get('generated_text', '')
            return get_fallback_response(text)
        elif response.status_code == 503:
            st.warning("Model is loading... Please Wait")
            time.sleep(5)
            return get_fallback_response(text)
        else:
            st.error(f"API Error: Status code {response.status_code}")
            return get_fallback_response(text)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return get_fallback_response(text)

# Function to test API connection from the sidebar
def test_api_connection():
    try:
        test_response = query_huggingface("Generate a short motivational message")
        if test_response and not test_response.startswith("API Error"):
            return True, "API connection successful"
        return False, "API connection failed"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

# Button in the sidebar to test API
with st.sidebar:
    if st.button("Test API Connection"):
        with st.spinner("Testing..."):
            is_connected, message = test_api_connection()
            if is_connected:
                st.success(message)
            else:
                st.error(message)

# Fallback response for AI when API fails or text not detected
def get_fallback_response(prompt):
    responses = {
        "mission": [
            "Explore the unknown corners of your creativity.",
            "Launch your passion project today.",
            "Your mission: Design something bold and impactful!"
        ],
        "challenge": [
            "Take the 30-day UI challenge and level up your skills!",
            "Post daily for 30 days—consistency builds confidence.",
            "Complete one design challenge per day—no excuses!"
        ],
        "motivation": [
            "You are capable of amazing things. Keep going!",
            "Every step forward is progress—stay consistent!",
            "Push through today for a better tomorrow."
        ]
    }

    if "mission" in prompt.lower():
        return random.choice(responses["mission"])
    elif "challenge" in prompt.lower():
        return random.choice(responses["challenge"])
    else:
        return random.choice(responses["motivation"])

# Sidebar input for explorer name and mission count
with st.sidebar:
    st.title("Mission Control")
    if 'explorer_name' not in st.session_state:
        st.session_state.explorer_name = st.text_input("Enter Explorer Name", "Space Pioneer")

    st.subheader("Mission Starts")
    if 'mission_completed' not in st.session_state:
        st.session_state.mission_completed = 0

# Display number of missions launched
st.metric("Missions Launched", st.session_state.mission_completed)

# Explorer Rank logic
st.subheader("Explorer Rank")
ranks = {
    5: 'Cosmic Rookie',
    10: 'Star Navigator',
    15: 'Galaxy Pioneer',
    20: 'Universal Master'
}

current_rank = max([level for level in ranks if st.session_state.mission_completed >= level], default=0)

if current_rank > 0:
    st.markdown(f"<div class='achievement-badge'>{ranks[current_rank]}</div>", unsafe_allow_html=True)

# Main Title
st.title("Mindset Explorer")
st.write(f"Welcome, Explorer {st.session_state.explorer_name}! Ready for your next mission?")

# Mission Planning
with st.container():
    st.subheader("Launching a New Mission")
    mission = st.text_input("Enter your mission", placeholder="e.g. Design a new app interface...")
    if st.button("Mission Plan"):
        if mission:
            with st.spinner("Generating mission plan..."):
                refined_mission = query_huggingface({"inputs": f"Refine this mission: {mission}"})
                strategy = query_huggingface({"inputs": f"Create a 30 days strategy for this mission: {mission}"})
                cosmic_wisdom = query_huggingface({"inputs": f"Generate a cosmic wisdom quote for this mission: {mission}"})

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("Mission Plan")
                    st.write(refined_mission)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("30-Day Strategy")
                    st.write(strategy)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='quote-box'>", unsafe_allow_html=True)
                st.write(f"*{cosmic_wisdom}*")
                st.markdown("</div>", unsafe_allow_html=True)

                st.session_state.mission_completed += 1
        else:
            st.warning("Please enter a mission to proceed.")

# Initialize progress tracking if not present
if 'mission_progress' not in st.session_state:
    st.session_state.mission_progress = [False] * 30

# Progress header
st.header("Mission Progress")

# Show 30 day progress tracker using checkboxes
progress_cols = st.columns(10)
for i in range(30):
    col_index = i % 10
    with progress_cols[col_index]:
        milestone_class = "progress-milestone milestone-active" if st.session_state.mission_progress[i] else "progress-milestone"
        st.markdown(f"<div class='{milestone_class}'>", unsafe_allow_html=True)
        checkbox_value = st.checkbox(f"D{i+1}", value=st.session_state.mission_progress[i], key=f"day_{i+1}")
        st.markdown("</div>", unsafe_allow_html=True)
        if checkbox_value != st.session_state.mission_progress[i]:
            st.session_state.mission_progress[i] = checkbox_value
            st.rerun()

# Calculate and display progress
day_complete = sum(st.session_state.mission_progress)
progress_percentage = (day_complete / 30) * 100

st.progress(progress_percentage / 100)
st.write(f"Mission Progress: {day_complete}/30 milestones achieved! ({progress_percentage:.1f}%)")

# Mission Status messages
if progress_percentage == 100:
    st.balloons()
    st.success("Mission Completed! You have completed all milestones.")
elif progress_percentage >= 75:
    st.info("Final Approach initiated! Keep pushing forward.")
elif progress_percentage >= 50:
    st.info("Over halfway there! Keep up the momentum.")
elif progress_percentage >= 25:
    st.info("You're getting started. Good pace!")
else:
    st.info("Pre-launch info sequence initiated! Ready for takeoff.")

# Cosmic Tips Section
st.header("Cosmic Wisdom")
cosmic_tips = [
    "Consistency is your rocket fuel.",
    "Each small step brings you closer to greatness.",
    "Explore beyond the stars of doubt.",
    "Let your creativity shine like a supernova!",
    "Break through mental gravity.",
    "Design. Launch. Repeat."
]

st.write(random.choice(cosmic_tips))
