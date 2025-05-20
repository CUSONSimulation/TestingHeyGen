import requests
import json
import time
import os
import streamlit as st

class HeyGenAPI:
    """
    Class to handle interactions with the HeyGen API for avatar animation and streaming.
    
    This integrates with HeyGen's API to create and animate virtual avatars
    for the nursing simulation.
    """
    
    def __init__(self, api_key=None):
        """Initialize the HeyGen API client with authentication."""
        self.api_key = api_key or os.environ.get('HEYGEN_API_KEY')
        if not self.api_key:
            st.error("HeyGen API key not found. Please set the HEYGEN_API_KEY environment variable.")
        
        self.base_url = "https://api.heygen.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Cache for avatar IDs
        self.avatar_cache = {}
    
    def get_avatar(self, avatar_name):
        """
        Get or create an avatar for use in the simulation.
        
        Args:
            avatar_name: Name of the avatar ("sam" for Sam Richards or "instructor")
            
        Returns:
            avatar_id: ID of the avatar to use in other API calls
        """
        # Check if we already have this avatar cached
        if avatar_name in self.avatar_cache:
            return self.avatar_cache[avatar_name]
        
        # In a real implementation, you would either:
        # 1. Create a new avatar using the HeyGen API
        # 2. Use an existing avatar ID that you've created in the HeyGen dashboard
        
        # For now, we'll use placeholder IDs (these should be replaced with real IDs)
        avatar_ids = {
            "sam": "avatar_sam_richards_id",  # Replace with actual ID
            "instructor": "avatar_noa_martinez_id"  # Replace with actual ID
        }
        
        if avatar_name in avatar_ids:
            self.avatar_cache[avatar_name] = avatar_ids[avatar_name]
            return avatar_ids[avatar_name]
        else:
            st.error(f"Avatar '{avatar_name}' not found.")
            return None
    
    def animate_avatar_speech(self, avatar_name, text):
        """
        Generate an animated video of the avatar speaking the provided text.
        
        Args:
            avatar_name: Name of the avatar to animate ("sam" or "instructor")
            text: The text for the avatar to speak
            
        Returns:
            video_url: URL to the generated video (or stream) that can be embedded
        """
        avatar_id = self.get_avatar(avatar_name)
        
        if not avatar_id:
            return None
        
        try:
            # Endpoint for creating a talking avatar video
            endpoint = f"{self.base_url}/talking-avatar"
            
            # Prepare the request payload according to HeyGen API documentation
            payload = {
                "avatar_id": avatar_id,
                "text": text,
                "voice_id": self._get_voice_id_for_avatar(avatar_name),
                "output_format": "mp4",  # Or whatever format is supported
                "streaming": True  # Enable streaming for real-time interaction
            }
            
            # Make the API request
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # In a real implementation, you would handle the response structure per
            # the HeyGen API documentation
            
            # For now, we'll return a placeholder URL
            # This should be replaced with the actual video URL from the response
            return "https://example.com/avatar_video.mp4"
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error generating avatar speech: {str(e)}")
            return None
    
    def get_stream_url(self, job_id):
        """
        Get the streaming URL for a previously created job.
        
        Args:
            job_id: ID of the job returned from animate_avatar_speech
            
        Returns:
            stream_url: URL to the video stream
        """
        try:
            # Endpoint for getting job status/result
            endpoint = f"{self.base_url}/jobs/{job_id}"
            
            # Check job status
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            # If the job is complete, return the stream URL
            if result.get("status") == "completed":
                return result.get("stream_url")
            
            # If not complete, return None (caller should retry)
            return None
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error checking job status: {str(e)}")
            return None
    
    def _get_voice_id_for_avatar(self, avatar_name):
        """
        Get the appropriate voice ID for each avatar.
        
        Args:
            avatar_name: Name of the avatar ("sam" or "instructor")
            
        Returns:
            voice_id: ID of the voice to use
        """
        # In a real implementation, you would use the appropriate voice IDs
        # from HeyGen for each character
        voice_ids = {
            "sam": "male_middle_aged_stern_voice_id",  # Replace with actual ID
            "instructor": "professional_instructor_voice_id"  # Replace with actual ID
        }
        
        return voice_ids.get(avatar_name, "default_voice_id")