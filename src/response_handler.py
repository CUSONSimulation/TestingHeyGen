import random
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
import streamlit as st

# Download necessary NLTK data (in a real app, this would be done during setup)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResponseHandler:
    """
    Class to handle determining appropriate responses from Sam Richards
    based on user input, following natural conversation principles.
    """
    
    def __init__(self, simulation_script):
        """
        Initialize the response handler with the simulation script.
        
        Args:
            simulation_script: JSON object containing Sam's character info and responses
        """
        self.script = simulation_script
        self.responses = simulation_script['responses']
        self.character = simulation_script['character']
        
        # Track which response categories have been used
        self.used_categories = set()
        
        # Keywords that trigger specific responses
        self.keywords = {
            "staff": ["staffing_issues"],
            "officer": ["staffing_issues"],
            "manpower": ["staffing_issues"],
            "security": ["security_concerns"],
            "risk": ["security_concerns", "inmate_resistance"],
            "space": ["space_limitations"],
            "room": ["space_limitations"],
            "facility": ["space_limitations", "security_concerns"],
            "paperwork": ["paperwork_burden"],
            "documentation": ["paperwork_burden"],
            "consent": ["paperwork_burden", "inmate_resistance"],
            "budget": ["budget_concerns"],
            "cost": ["budget_concerns"],
            "money": ["budget_concerns"],
            "expense": ["budget_concerns"],
            "inmate": ["inmate_resistance"],
            "refuse": ["inmate_resistance"],
            "voluntary": ["inmate_resistance"],
            "schedule": ["scheduling_disruptions"],
            "time": ["scheduling_disruptions"],
            "routine": ["scheduling_disruptions"],
            "previous": ["past_failures"],
            "before": ["past_failures"],
            "last year": ["past_failures"],
            "evidence": ["evidence_response"],
            "data": ["evidence_response"],
            "research": ["evidence_response"],
            "alternative": ["alternative_suggestions"],
            "option": ["alternative_suggestions"],
            "compromise": ["alternative_suggestions"],
        }
        
        # Initialize previous responses to avoid repetition
        self.previous_responses = []
        
        # Store the most recent user input for natural follow-ups
        self.last_user_input = ""
        
        # Store key phrases from conversation for callbacks/references
        self.conversation_key_phrases = []
        
        # Initialize conversation state
        self.conversation_state = {
            "resistance_level": 3,  # Scale of 1-5, 5 being most resistant
            "current_topic": None,
            "topics_addressed": set(),
            "last_response_category": None,
            "conversation_depth": 0,  # Tracks how deep we are in the conversation
            "mentioned_points": set(),  # Key points that have been mentioned
            "emotions_expressed": [],  # Emotions that Sam has expressed
        }
        
        # Transition phrases for more natural flow
        self.transitions = [
            "Look,",
            "Thing is,",
            "Here's the deal -",
            "Listen,",
            "Let me be clear -",
            "I gotta say,",
            "Honestly,",
            "Between us,",
            "The way I see it,",
            "Let's be real here -"
        ]
        
        # Follow-up phrases to create continuity
        self.follow_ups = [
            "And another thing -",
            "Plus,",
            "Not to mention",
            "That's not even considering",
            "And don't get me started on",
            "Which reminds me -"
        ]
        
        # Expressions of uncertainty for natural human-like responses
        self.uncertainty_phrases = [
            "I'm not sure about that.",
            "I haven't thought about it that way.",
            "I'd need to see some proof before I buy that.",
            "That sounds questionable to me.",
            "I'm skeptical, to be honest."
        ]
        
        # Contractions and natural speech patterns to replace formal speech
        self.speech_naturalizers = {
            "I am": "I'm",
            "you are": "you're",
            "we are": "we're",
            "they are": "they're",
            "is not": "isn't",
            "are not": "aren't",
            "was not": "wasn't",
            "were not": "weren't",
            "have not": "haven't",
            "has not": "hasn't",
            "had not": "hadn't",
            "will not": "won't",
            "would not": "wouldn't",
            "could not": "couldn't",
            "should not": "shouldn't",
            "cannot": "can't",
            "do not": "don't",
            "does not": "doesn't",
            "did not": "didn't"
        }
    
    def get_response(self, category):
        """
        Get a natural-sounding response from the specified category.
        
        Args:
            category: The response category to select from
            
        Returns:
            A string response from Sam Richards with natural conversation elements
        """
        if category in self.responses and self.responses[category]:
            # Get all available responses in this category
            available_responses = self.responses[category]
            
            # Filter out recently used responses to avoid repetition
            filtered_responses = [r for r in available_responses 
                                 if r not in self.previous_responses[-3:]]
            
            # If all responses have been recently used, reset and use any
            if not filtered_responses:
                filtered_responses = available_responses
            
            # Select a random response
            response = random.choice(filtered_responses)
            
            # Update tracking
            self.previous_responses.append(response)
            self.used_categories.add(category)
            self.conversation_state["last_response_category"] = category
            
            # Natural language enhancement
            response = self.naturalize_response(response, category)
            
            return response
        else:
            # Fallback response if category not found
            return self.naturalize_response("I'm not sure what to say about that. Let's get back to discussing this vaccination program.", "fallback")
    
    def naturalize_response(self, response, category):
        """
        Make the response more natural-sounding by adding conversation elements.
        
        Args:
            response: The base response text
            category: The category of the response
        
        Returns:
            Enhanced natural-sounding response
        """
        # Don't modify opening interactions too much
        if category == "opening_interaction":
            return response
        
        # Sometimes add a transition phrase at the beginning
        if random.random() < 0.4 and not response.startswith("Look") and not response.startswith("Listen"):
            response = f"{random.choice(self.transitions)} {response}"
        
        # Sometimes reference a previous point for continuity
        if (self.conversation_state["conversation_depth"] > 2 and 
            random.random() < 0.3 and 
            len(self.conversation_key_phrases) > 0):
            
            previous_point = random.choice(self.conversation_key_phrases)
            follow_up = random.choice([
                f"Getting back to what I said about {previous_point}, ",
                f"As I mentioned about {previous_point}, ",
                f"That's related to the {previous_point} issue I mentioned. "
            ])
            
            sentences = sent_tokenize(response)
            if len(sentences) > 1:
                # Insert the follow-up at a sensible point in the response
                insert_point = random.randint(1, min(2, len(sentences)-1))
                sentences.insert(insert_point, follow_up)
                response = " ".join(sentences)
        
        # Apply contractions for more natural speech
        for formal, contraction in self.speech_naturalizers.items():
            response = re.sub(r'\b' + formal + r'\b', contraction, response, flags=re.IGNORECASE)
        
        # Sometimes express uncertainty (only for certain categories)
        uncertain_categories = ["evidence_response", "alternative_suggestions"]
        if category in uncertain_categories and random.random() < 0.3:
            sentences = sent_tokenize(response)
            if len(sentences) > 2:
                insert_point = random.randint(1, len(sentences)-1)
                sentences.insert(insert_point, random.choice(self.uncertainty_phrases))
                response = " ".join(sentences)
        
        # Track a key phrase from this response for future callbacks
        words = response.split()
        if len(words) > 5:
            # Find a potential key phrase (3-5 word segment)
            phrase_length = min(random.randint(3, 5), len(words) - 1)
            start_idx = random.randint(0, len(words) - phrase_length)
            key_phrase = " ".join(words[start_idx:start_idx + phrase_length])
            self.conversation_key_phrases.append(key_phrase)
            
            # Keep the list manageable
            if len(self.conversation_key_phrases) > 5:
                self.conversation_key_phrases.pop(0)
                
        return response
    
    def extract_key_points(self, text):
        """
        Extract potential key points from the user's input for future reference.
        
        Args:
            text: User input text
            
        Returns:
            List of extracted key points
        """
        # Simple extraction - in a real implementation this would be more sophisticated
        sentences = sent_tokenize(text)
        key_points = []
        
        for sentence in sentences:
            # Look for sentences with keywords that might be important
            if any(keyword in sentence.lower() for keyword in 
                  ["important", "critical", "necessary", "need", "should", 
                   "must", "benefit", "advantage", "solution"]):
                key_points.append(sentence)
        
        return key_points
    
    def process_user_input(self, user_input):
        """
        Process user input and determine an appropriate response.
        
        Args:
            user_input: The text input from the user/student
            
        Returns:
            A string response from Sam Richards
        """
        # Store the user input for future reference
        self.last_user_input = user_input
        
        # Extract key points for potential callbacks
        key_points = self.extract_key_points(user_input)
        for point in key_points:
            if len(point.split()) > 3:  # Only store substantive points
                self.conversation_key_phrases.append(point)
        
        # Increment conversation depth
        self.conversation_state["conversation_depth"] += 1
        
        # Convert to lowercase for processing
        text = user_input.lower()
        
        # Tokenize the input
        tokens = word_tokenize(text)
        
        # Remove punctuation and stopwords for better keyword matching
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if w not in string.punctuation]
        
        # Identify matching keywords and their categories
        matching_categories = []
        for token in tokens:
            for keyword, categories in self.keywords.items():
                if keyword in token or token in keyword:
                    matching_categories.extend(categories)
        
        # Check for phrases (multi-word keywords)
        for keyword, categories in self.keywords.items():
            if ' ' in keyword and keyword in text:
                matching_categories.extend(categories)
        
        # Remove duplicates
        matching_categories = list(set(matching_categories))
        
        # Add some natural variation to response selection
        
        # If this is early in the conversation (few topics addressed)
        if self.conversation_state["conversation_depth"] < 3:
            # More likely to be dismissive and resistant
            if "opening_interaction" not in self.used_categories and not matching_categories:
                return self.get_response("opening_interaction")
        
        # Sometimes directly address what the user just said
        if random.random() < 0.3 and self.last_user_input:
            # Extract a snippet from their input to reference
            words = self.last_user_input.split()
            if len(words) > 4:
                start_idx = random.randint(0, min(8, len(words) - 3))
                snippet_length = min(random.randint(3, 5), len(words) - start_idx)
                snippet = " ".join(words[start_idx:start_idx + snippet_length])
                
                reference_responses = [
                    f"When you say '{snippet},' that's exactly the kind of thinking that doesn't work here.",
                    f"'{snippet}'? That sounds good in theory, but in practice...",
                    f"I hear you talking about '{snippet},' but you're missing the bigger picture.",
                    f"That part about '{snippet}' - that's where I have concerns."
                ]
                
                # 30% chance to directly reference their words
                if random.random() < 0.3 and matching_categories:
                    return random.choice(reference_responses) + " " + self.get_response(random.choice(matching_categories))
        
        # If user mentions topics we haven't discussed yet
        new_topics = [cat for cat in matching_categories 
                     if cat not in self.conversation_state["topics_addressed"]]
        
        if new_topics:
            # Update topics addressed
            self.conversation_state["topics_addressed"].update(new_topics)
            # Choose one of the new topics to respond to
            return self.get_response(random.choice(new_topics))
        
        # As the conversation progresses, potentially become slightly more amenable
        if self.conversation_state["conversation_depth"] > 6:
            # Gradually reduce resistance level
            self.conversation_state["resistance_level"] = max(1, self.conversation_state["resistance_level"] - 0.2)
        
        # If we've addressed many topics but user isn't suggesting alternatives
        if (len(self.conversation_state["topics_addressed"]) >= 4 and
            "alternative_suggestions" not in self.used_categories and
            random.random() < 0.3):
            return self.get_response("alternative_suggestions")
        
        # If we've gone through most objections, move toward closing
        if (len(self.conversation_state["topics_addressed"]) >= 5 and
            "closing_remarks" not in self.used_categories and
            random.random() < 0.4):
            return self.get_response("closing_remarks")
        
        # If we have matching categories, choose one
        if matching_categories:
            return self.get_response(random.choice(matching_categories))
        
        # If no specific categories match, choose a random category
        # that hasn't been used much
        unused_categories = [cat for cat in self.responses.keys() 
                            if cat not in self.used_categories]
        
        if unused_categories:
            return self.get_response(random.choice(unused_categories))
        
        # If all else fails, use evidence_response as a fallback
        return self.get_response("evidence_response")