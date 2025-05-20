import streamlit as st
import json

class SpeechRecognizer:
    """
    Class to handle speech-to-text conversion using browser-based recognition.
    
    This class provides an interface for capturing user speech and converting
    it to text for processing in the simulation.
    """
    
    def __init__(self):
        """Initialize the speech recognizer."""
        pass
    
    def setup_speech_recognition(self):
        """
        Set up browser-based speech recognition components.
        
        Returns:
            HTML/JavaScript code for speech recognition that can be embedded in Streamlit
        """
        # Create a JavaScript component for speech recognition
        # This uses the Web Speech API which is supported in most modern browsers
        speech_recognition_html = """
        <script>
        // Speech recognition configuration
        let recognition;
        let finalTranscript = '';
        let isRecognizing = false;
        
        // Initialize speech recognition
        function initializeSpeechRecognition() {
            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
            } else if ('SpeechRecognition' in window) {
                recognition = new SpeechRecognition();
            } else {
                document.getElementById('status').innerHTML = 'Speech recognition not supported in this browser';
                return;
            }
            
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isRecognizing = true;
                document.getElementById('status').innerHTML = 'Listening...';
                document.getElementById('microphone-btn').classList.add('recording');
            };
            
            recognition.onend = function() {
                isRecognizing = false;
                document.getElementById('status').innerHTML = 'Click to start speaking';
                document.getElementById('microphone-btn').classList.remove('recording');
            };
            
            recognition.onresult = function(event) {
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                document.getElementById('speech-text').value = finalTranscript + interimTranscript;
            };
            
            recognition.onerror = function(event) {
                document.getElementById('status').innerHTML = 'Error occurred: ' + event.error;
            };
        }
        
        // Toggle speech recognition
        function toggleSpeechRecognition() {
            if (!recognition) {
                initializeSpeechRecognition();
            }
            
            if (isRecognizing) {
                recognition.stop();
            } else {
                finalTranscript = '';
                document.getElementById('speech-text').value = '';
                recognition.start();
            }
        }
        
        // Send the transcribed text to Streamlit
        function sendTranscriptToStreamlit() {
            const text = document.getElementById('speech-text').value;
            if (text.trim() !== '') {
                // Use Streamlit's setComponentValue to send data back to Python
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: text
                }, '*');
                
                // Reset transcript
                finalTranscript = '';
                document.getElementById('speech-text').value = '';
            }
        }
        </script>
        
        <div style="margin: 20px 0; padding: 15px; border-radius: 5px; background-color: #f0f2f6;">
            <div id="status" style="margin-bottom: 10px;">Click to start speaking</div>
            
            <button id="microphone-btn" onclick="toggleSpeechRecognition()" 
                    style="padding: 10px; border-radius: 50%; width: 50px; height: 50px; margin-right: 10px;">
                🎤
            </button>
            
            <textarea id="speech-text" style="width: 100%; height: 100px; margin: 10px 0; padding: 10px;"
                      placeholder="Your speech will appear here..."></textarea>
            
            <button onclick="sendTranscriptToStreamlit()" 
                    style="padding: 10px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">
                Send Response
            </button>
        </div>
        
        <style>
        #microphone-btn.recording {
            background-color: #ff4b4b;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        </style>
        """
        
        return speech_recognition_html
    
    def create_speech_input_component(self):
        """
        Create a Streamlit component for speech input.
        
        Returns:
            The transcribed text from user speech
        """
        # Create a unique key for the component
        component_key = "speech_recognition_component"
        
        # Create a container for the speech recognition component
        container = st.empty()
        
        # Inject the HTML/JavaScript for speech recognition
        container.markdown(self.setup_speech_recognition(), unsafe_allow_html=True)
        
        # Create a hidden text input to receive the transcribed speech
        # In a real implementation, you would use a custom component or the Streamlit 
        # component API to handle the data transfer
        
        # For now, we'll use a placeholder implementation
        # where the user can manually click "Send Response" in the UI
        
        return None  # This would normally return the transcribed text