import streamlit as st
import json
import os
import time
import random
from src.heygen_api import HeyGenAPI
from src.speech_to_text import SpeechRecognizer
from src.response_handler import ResponseHandler
from src.instructor_response_handler import InstructorResponseHandler
from src.utils import save_conversation_history, generate_feedback, create_evaluation_report

# Page configuration
st.set_page_config(
    page_title="Nursing Simulation - Corrections Facility",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'introduction'
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'simulation_started' not in st.session_state:
    st.session_state.simulation_started = False
if 'prebrief_completed' not in st.session_state:
    st.session_state.prebrief_completed = False
if 'debrief_started' not in st.session_state:
    st.session_state.debrief_started = False
if 'prebrief_conversation' not in st.session_state:
    st.session_state.prebrief_conversation = []
if 'debrief_conversation' not in st.session_state:
    st.session_state.debrief_conversation = []
if 'response_handler' not in st.session_state:
    # Load the simulation script
    with open('assets/scripts/simulation_script.json', 'r') as f:
        simulation_script = json.load(f)
    st.session_state.response_handler = ResponseHandler(simulation_script)
if 'instructor_handler' not in st.session_state:
    # Load the instructor scripts
    try:
        with open('assets/scripts/prebrief_script.json', 'r') as f:
            prebrief_script = json.load(f)
        with open('assets/scripts/debrief_script.json', 'r') as f:
            debrief_script = json.load(f)
        st.session_state.prebrief_handler = InstructorResponseHandler(prebrief_script)
        st.session_state.debrief_handler = InstructorResponseHandler(debrief_script)
    except FileNotFoundError:
        st.error("Script files not found. Please check your file paths.")

# Initialize API clients
heygen_api = HeyGenAPI(api_key=os.environ.get('HEYGEN_API_KEY'))
speech_recognizer = SpeechRecognizer()

# Navigation functions
def go_to_introduction():
    st.session_state.current_page = 'introduction'

def go_to_prebrief():
    st.session_state.current_page = 'prebrief'

def go_to_simulation():
    st.session_state.current_page = 'simulation'
    st.session_state.simulation_started = True

def go_to_debrief():
    st.session_state.current_page = 'debrief'
    st.session_state.debrief_started = True

def go_to_summary():
    st.session_state.current_page = 'summary'

# Create sidebar navigation
with st.sidebar:
    st.title("Simulation Navigation")
    st.button("Introduction", on_click=go_to_introduction)
    st.button("Pre-Brief", on_click=go_to_prebrief)
    st.button("Simulation", on_click=go_to_simulation)
    st.button("De-Brief", on_click=go_to_debrief)
    st.button("Summary", on_click=go_to_summary)
    
    st.markdown("---")
    st.markdown("### Simulation Controls")
    if st.button("Reset Simulation"):
        st.session_state.conversation_history = []
        st.session_state.prebrief_conversation = []
        st.session_state.debrief_conversation = []
        st.session_state.simulation_started = False
        st.session_state.prebrief_completed = False
        st.session_state.debrief_started = False
        st.success("Simulation has been reset!")

# Introduction Page
if st.session_state.current_page == 'introduction':
    st.title("Flu Vaccination in Corrections Simulation")
    
    st.markdown("""
    ## Welcome to the Interactive Nursing Simulation!
    
    In this simulation, you will take on the role of a public health nurse trying to implement 
    a flu vaccination program in a county corrections facility. You will be meeting with 
    **Sam Richards**, the Operations Manager, who is known to be resistant to change.
    
    This simulation uses natural conversation technology to create realistic interactions 
    with both Sam Richards and your instructor, Noa Martinez.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Your Objectives:
        - Convince Sam of the importance of the flu vaccination program
        - Address concerns and objections constructively
        - Find a workable solution for implementation
        - Apply change management principles in real-time
        """)
    
    with col2:
        st.markdown("""
        ### How It Works:
        1. First, you'll receive a pre-briefing from Noa Martinez
        2. Then, you'll interact with Sam Richards using speech-to-speech technology
        3. After the simulation, you'll participate in a debriefing session with Noa
        """)
    
    if st.button("Start Pre-Brief"):
        go_to_prebrief()

# Pre-brief Page
elif st.session_state.current_page == 'prebrief':
    st.title("Pre-Brief with Noa Martinez")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # This would be replaced with the HeyGen avatar for Noa Martinez
        st.image("https://via.placeholder.com/400x400.png?text=Noa+Martinez", 
                 caption="Noa Martinez - Nursing Faculty")
    
    with col2:
        conversation_container = st.container()
        with conversation_container:
            # Display conversation history
            for entry in st.session_state.prebrief_conversation:
                if entry['speaker'] == 'user':
                    st.markdown(f"**You:** {entry['text']}")
                else:
                    st.markdown(f"**Noa:** {entry['text']}")
            
            # Initial greeting if prebrief just started
            if len(st.session_state.prebrief_conversation) == 0:
                # Get an initial response from Noa
                initial_response = st.session_state.prebrief_handler.generate_prebrief_response("introduction")
                st.session_state.prebrief_conversation.append({
                    'speaker': 'instructor',
                    'text': initial_response
                })
                
                # In a real implementation, this would trigger the HeyGen avatar to speak
                # heygen_api.animate_avatar_speech("instructor", initial_response)
                
                st.markdown(f"**Noa says:** {initial_response}")
    
    # User input for talking to Noa
    st.markdown("### Ask Noa Questions:")
    
    # Simulating speech input with a text area for now
    user_input = st.text_area("Your question or comment:", height=100, 
                             placeholder="Ask a question or share your thoughts...")
    
    if st.button("Send to Noa"):
        if user_input:
            # Add user input to conversation history
            st.session_state.prebrief_conversation.append({
                'speaker': 'user',
                'text': user_input
            })
            
            # Get response from Noa based on user input
            noa_response = st.session_state.prebrief_handler.process_student_input(user_input, mode="prebrief")
            
            # Add Noa's response to conversation history
            st.session_state.prebrief_conversation.append({
                'speaker': 'instructor',
                'text': noa_response
            })
            
            # In a real implementation, this would trigger the HeyGen avatar to speak
            # heygen_api.animate_avatar_speech("instructor", noa_response)
            
            # Force page refresh to show updated conversation
            st.experimental_rerun()
    
    # Check if we've had enough exchanges to offer to move to simulation
    if len(st.session_state.prebrief_conversation) >= 4:  # After a few exchanges
        st.session_state.prebrief_completed = True
        
        if st.button("I'm Ready - Start Simulation"):
            go_to_simulation()

# Simulation Page
elif st.session_state.current_page == 'simulation':
    st.title("Simulation: Meeting with Sam Richards")
    
    # Main simulation interface
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # This would be replaced with the HeyGen avatar for Sam Richards
        st.image("https://via.placeholder.com/400x400.png?text=Sam+Richards", 
                 caption="Sam Richards - Operations Manager")
        
        # Display conversation history
        st.markdown("### Conversation History")
        conversation_container = st.container()
        with conversation_container:
            for i, entry in enumerate(st.session_state.conversation_history):
                if entry['speaker'] == 'user':
                    st.markdown(f"**You:** {entry['text']}")
                else:
                    st.markdown(f"**Sam:** {entry['text']}")
    
    with col2:
        st.markdown("### Interact with Sam")
        
        # Initial greeting if simulation just started
        if st.session_state.simulation_started and len(st.session_state.conversation_history) == 0:
            # Get an opening response from Sam
            opening_response = st.session_state.response_handler.get_response("opening_interaction")
            st.session_state.conversation_history.append({
                'speaker': 'sam',
                'text': opening_response
            })
            
            # In a real implementation, this would trigger the HeyGen avatar to speak
            # heygen_api.animate_avatar_speech("sam", opening_response)
            
            st.markdown(f"**Sam says:** {opening_response}")
        
        # Speech to text input (placeholder - would be replaced with actual speech recognition)
        st.markdown("### Speak to Sam:")
        
        # Simulating speech input with a text area for now
        user_input = st.text_area("Your response to Sam:", height=100, 
                                 placeholder="Type what you would say to Sam...")
        
        if st.button("Send Response"):
            if user_input:
                # Add user input to conversation history
                st.session_state.conversation_history.append({
                    'speaker': 'user',
                    'text': user_input
                })
                
                # Get response from Sam based on user input
                sam_response = st.session_state.response_handler.process_user_input(user_input)
                
                # Add Sam's response to conversation history
                st.session_state.conversation_history.append({
                    'speaker': 'sam',
                    'text': sam_response
                })
                
                # In a real implementation, this would trigger the HeyGen avatar to speak
                # heygen_api.animate_avatar_speech("sam", sam_response)
                
                # Force page refresh to show updated conversation
                st.experimental_rerun()
        
        # Option to end simulation and go to debrief
        if len(st.session_state.conversation_history) >= 6:  # After a few exchanges
            if st.button("End Simulation and Go to Debrief"):
                # Save the conversation for analysis
                save_conversation_history(st.session_state.conversation_history)
                go_to_debrief()

# Debrief Page
elif st.session_state.current_page == 'debrief':
    st.title("Debriefing Session with Noa Martinez")
    
    # Main debrief interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # This would be replaced with the HeyGen avatar for Noa Martinez
        st.image("https://via.placeholder.com/400x400.png?text=Noa+Martinez", 
                 caption="Noa Martinez - Nursing Faculty")
        
        # Display a summary of the simulation
        st.markdown("### Simulation Summary")
        with st.expander("View Conversation with Sam", expanded=False):
            for i, entry in enumerate(st.session_state.conversation_history):
                if entry['speaker'] == 'user':
                    st.markdown(f"**You:** {entry['text']}")
                else:
                    st.markdown(f"**Sam:** {entry['text']}")
    
    with col2:
        conversation_container = st.container()
        with conversation_container:
            # Display debrief conversation history
            for entry in st.session_state.debrief_conversation:
                if entry['speaker'] == 'user':
                    st.markdown(f"**You:** {entry['text']}")
                else:
                    st.markdown(f"**Noa:** {entry['text']}")
            
            # Initial greeting if debrief just started
            if len(st.session_state.debrief_conversation) == 0:
                # Get an initial debrief response from Noa
                initial_response = st.session_state.debrief_handler.generate_debrief_response("introduction")
                st.session_state.debrief_conversation.append({
                    'speaker': 'instructor',
                    'text': initial_response
                })
                
                # In a real implementation, this would trigger the HeyGen avatar to speak
                # heygen_api.animate_avatar_speech("instructor", initial_response)
                
                st.markdown(f"**Noa says:** {initial_response}")
        
        # User input for talking to Noa
        st.markdown("### Discuss with Noa:")
        
        # Simulating speech input with a text area for now
        user_input = st.text_area("Your reflection or question:", height=100, 
                                 placeholder="Share your thoughts about the simulation...")
        
        if st.button("Send to Noa"):
            if user_input:
                # Add user input to conversation history
                st.session_state.debrief_conversation.append({
                    'speaker': 'user',
                    'text': user_input
                })
                
                # Get response from Noa based on user input
                noa_response = st.session_state.debrief_handler.process_student_input(user_input, mode="debrief")
                
                # Add Noa's response to conversation history
                st.session_state.debrief_conversation.append({
                    'speaker': 'instructor',
                    'text': noa_response
                })
                
                # In a real implementation, this would trigger the HeyGen avatar to speak
                # heygen_api.animate_avatar_speech("instructor", noa_response)
                
                # Force page refresh to show updated conversation
                st.experimental_rerun()
    
    # Check if we've had enough exchanges to offer to move to summary
    if len(st.session_state.debrief_conversation) >= 6:  # After a few exchanges
        if st.button("Complete Debrief and View Summary"):
            go_to_summary()

# Summary Page
elif st.session_state.current_page == 'summary':
    st.title("Simulation Summary")
    
    # Generate feedback based on the simulation
    feedback = generate_feedback(st.session_state.conversation_history)
    
    st.markdown("""
    ## Thank you for completing the simulation!
    
    Your interactions with both Sam Richards and Noa Martinez have been evaluated to provide you 
    with personalized feedback and insights.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Conversation Metrics")
        st.markdown(f"- **Total exchanges with Sam:** {feedback['metrics']['conversation_length']}")
        st.markdown(f"- **Your responses:** {feedback['metrics']['user_turns']}")
        st.markdown(f"- **Average response length:** {int(feedback['metrics']['average_user_response_length'])} characters")
        
        st.markdown("### Key Strengths")
        for strength in feedback['strengths']:
            st.markdown(f"- {strength}")
    
    with col2:
        st.markdown("### Areas for Improvement")
        for area in feedback['areas_for_improvement']:
            st.markdown(f"- {area}")
        
        st.markdown("### Overall Assessment")
        st.markdown(feedback['overall_assessment'])
    
    st.markdown("### Complete Conversation Record")
    tab1, tab2, tab3 = st.tabs(["Simulation with Sam", "Pre-Brief with Noa", "De-Brief with Noa"])
    
    with tab1:
        for entry in st.session_state.conversation_history:
            if entry['speaker'] == 'user':
                st.markdown(f"**You:** {entry['text']}")
            else:
                st.markdown(f"**Sam:** {entry['text']}")
    
    with tab2:
        for entry in st.session_state.prebrief_conversation:
            if entry['speaker'] == 'user':
                st.markdown(f"**You:** {entry['text']}")
            else:
                st.markdown(f"**Noa:** {entry['text']}")
    
    with tab3:
        for entry in st.session_state.debrief_conversation:
            if entry['speaker'] == 'user':
                st.markdown(f"**You:** {entry['text']}")
            else:
                st.markdown(f"**Noa:** {entry['text']}")
    
    if st.button("Start a New Simulation"):
        st.session_state.conversation_history = []
        st.session_state.prebrief_conversation = []
        st.session_state.debrief_conversation = []
        st.session_state.simulation_started = False
        st.session_state.prebrief_completed = False
        st.session_state.debrief_started = False
        go_to_introduction()

# Add CSS for better styling
st.markdown("""
<style>
    .stButton button {
        width: 100%;
    }
    .stSidebar .stButton button {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)