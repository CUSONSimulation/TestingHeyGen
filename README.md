# Nursing Simulation: Flu Vaccination in Corrections

An interactive simulation for nursing students to practice change management skills in a corrections setting, featuring a virtual avatar powered by HeyGen's API.

## Overview

This application provides a realistic simulation where nursing students take on the role of a public health nurse trying to implement a flu vaccination program in a corrections facility. Students interact with Sam Richards, a skeptical operations manager, using speech-to-speech technology.

The simulation follows this flow:
1. Introduction to the scenario
2. Pre-brief with Noa Martinez (instructor avatar)
3. Interactive simulation with Sam Richards
4. Debrief and reflection with Noa Martinez
5. Summary and evaluation

## Features

- Real-time speech-to-speech interaction with virtual avatars
- Natural conversation framework for authentic dialogue
- Character-driven responses based on a realistic script
- Natural language processing to determine appropriate responses
- Structured evaluation and reflection process
- HeyGen API integration for lifelike avatar animations

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A HeyGen API subscription and API key
- Git

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/nursing-simulation.git
   cd nursing-simulation
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   HEYGEN_API_KEY=your_heygen_api_key_here
   ```

5. Create necessary directories:
   ```bash
   mkdir -p assets/images assets/scripts data/conversations
   ```

6. Add your simulation script files to the assets/scripts directory

### Running the Application Locally

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Deploying to Streamlit.io

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Initial simulation setup"
   git push
   ```

2. Log in to [Streamlit.io](https://streamlit.io/)

3. Click "New app" and connect your GitHub repository

4. Set the necessary secrets (environment variables) for your app:
   - HEYGEN_API_KEY

5. Deploy your app

## HeyGen Integration

This application uses HeyGen's API to create and animate virtual avatars. You'll need to:

1. Create avatars in your HeyGen dashboard that match the characters (Sam Richards and Noa Martinez)
2. Note the avatar IDs and update them in `src/heygen_api.py`
3. Set up appropriate voices for each character

## Customizing the Simulation

### Modifying the Script

The simulation script is stored in `assets/scripts/simulation_script.json`. You can modify this file to change Sam's responses or add new response categories.

### Adding New Avatars

To add new avatars:

1. Create the avatar in your HeyGen dashboard
2. Add the avatar ID to the `get_avatar` method in `src/heygen_api.py`
3. Add appropriate voice configurations

### Extending Functionality

The modular structure allows for easy extensions:

- Add new simulation scenarios by creating new script files
- Implement more sophisticated response analysis in `src/response_handler.py`
- Enhance the evaluation metrics in `src/utils.py`

## Natural Conversation Framework

Both Sam Richards and Noa Martinez use a natural conversation framework that makes their interactions feel authentic rather than scripted. This is implemented through:

- Contextual awareness of previous statements
- Natural language patterns with contractions and varied sentence structures
- Dynamic references to student responses
- Emotional acknowledgment and adjustment
- Avoidance of bullet points and formal structures

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- HeyGen for their avatar API
- Streamlit for the web application framework
- NLTK for natural language processing capabilities