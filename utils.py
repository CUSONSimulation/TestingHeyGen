import os
import json
import time
import hashlib
import logging
import streamlit as st

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_script_file(filename):
    """
    Load a script JSON file from the assets directory.
    
    Args:
        filename: Name of the JSON file to load
        
    Returns:
        The loaded JSON content as a Python dict
    """
    try:
        file_path = os.path.join('assets', 'scripts', filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logger.error(f"Script file not found: {filename}")
        st.error(f"Script file not found: {filename}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in script file: {filename}")
        st.error(f"Invalid JSON in script file: {filename}")
        return None

def save_conversation_history(conversation_history, user_id=None):
    """
    Save the conversation history to a JSON file for future reference.
    
    Args:
        conversation_history: List of conversation entries
        user_id: Optional user identifier for the filename
        
    Returns:
        The path to the saved file
    """
    # Create a unique identifier if user_id not provided
    if not user_id:
        timestamp = int(time.time())
        user_id = f"user_{timestamp}"
    
    # Create directory if it doesn't exist
    os.makedirs('data/conversations', exist_ok=True)
    
    # Create filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"conversation_{user_id}_{timestamp}.json"
    file_path = os.path.join('data/conversations', filename)
    
    # Save conversation
    try:
        with open(file_path, 'w') as f:
            json.dump({
                'user_id': user_id,
                'timestamp': timestamp,
                'conversation': conversation_history
            }, f, indent=2)
        
        logger.info(f"Conversation saved to {file_path}")
        return file_path
    
    except Exception as e:
        logger.error(f"Failed to save conversation: {str(e)}")
        return None

def generate_feedback(conversation_history):
    """
    Generate automated feedback based on the conversation history.
    
    This is a placeholder for more sophisticated analysis in a real implementation.
    
    Args:
        conversation_history: List of conversation entries
        
    Returns:
        Dict containing feedback metrics and suggestions
    """
    # Count turns in conversation
    user_turns = sum(1 for entry in conversation_history if entry['speaker'] == 'user')
    
    # Basic metrics
    metrics = {
        'conversation_length': len(conversation_history),
        'user_turns': user_turns,
        'sam_turns': len(conversation_history) - user_turns,
        'average_user_response_length': sum(len(entry['text']) for entry in conversation_history 
                                          if entry['speaker'] == 'user') / max(user_turns, 1)
    }
    
    # In a real implementation, this would include more sophisticated analysis
    # such as sentiment analysis, keyword tracking, etc.
    
    # Basic feedback (placeholder)
    feedback = {
        'metrics': metrics,
        'strengths': [
            "You maintained a professional tone throughout the conversation.",
            "You persisted despite encountering resistance."
        ],
        'areas_for_improvement': [
            "Consider addressing underlying concerns more directly.",
            "Try using more data-driven arguments to support your position."
        ],
        'overall_assessment': "You demonstrated persistence in addressing resistance."
    }
    
    return feedback

def create_evaluation_report(conversation_history, user_reflection=None):
    """
    Create a comprehensive evaluation report for the simulation.
    
    Args:
        conversation_history: List of conversation entries
        user_reflection: Dict containing user's reflection responses
        
    Returns:
        HTML string containing the formatted report
    """
    # Generate automated feedback
    feedback = generate_feedback(conversation_history)
    
    # Create HTML report
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
        <h1>Simulation Evaluation Report</h1>
        <h2>Conversation Summary</h2>
        <p>Total exchanges: {feedback['metrics']['conversation_length']}</p>
        <p>User responses: {feedback['metrics']['user_turns']}</p>
        
        <h2>Strengths</h2>
        <ul>
    """
    
    # Add strengths
    for strength in feedback['strengths']:
        html += f"<li>{strength}</li>"
    
    html += """
        </ul>
        
        <h2>Areas for Improvement</h2>
        <ul>
    """
    
    # Add areas for improvement
    for area in feedback['areas_for_improvement']:
        html += f"<li>{area}</li>"
    
    html += f"""
        </ul>
        
        <h2>Overall Assessment</h2>
        <p>{feedback['overall_assessment']}</p>
    """
    
    # Add user reflection if available
    if user_reflection:
        html += """
        <h2>Self-Reflection</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <th style="text-align: left; padding: 8px; border-bottom: 1px solid #ddd;">Question</th>
                <th style="text-align: left; padding: 8px; border-bottom: 1px solid #ddd;">Response</th>
            </tr>
        """
        
        for question, response in user_reflection.items():
            html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{question}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{response}</td>
            </tr>
            """
        
        html += "</table>"
    
    html += """
    </div>
    """
    
    return html