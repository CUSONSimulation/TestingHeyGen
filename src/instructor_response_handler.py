import random
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import streamlit as st

class InstructorResponseHandler:
    """
    Class to handle natural, conversational responses from Noa Martinez (instructor).
    This creates authentic dialogue that avoids sounding scripted or robotic.
    """
    
    def __init__(self, instructor_script):
        """
        Initialize the instructor response handler with the script.
        
        Args:
            instructor_script: JSON object containing instructor info and responses
        """
        self.script = instructor_script
        self.sections = instructor_script['sections']
        self.instructor = instructor_script['instructor']
        
        # Track conversation progress
        self.current_section = None
        self.sections_covered = set()
        self.conversation_depth = 0
        
        # Store key phrases from user inputs for callbacks
        self.student_key_phrases = []
        
        # Track emotions observed in student responses
        self.observed_emotions = set()
        
        # Transition phrases for natural conversation flow
        self.transitions = [
            "Let's talk about",
            "I wanted to touch on",
            "Something worth considering is",
            "I've been thinking about",
            "It's interesting to note",
            "One thing that stands out is",
            "I'm curious about",
            "Let's explore"
        ]
        
        # Follow-up phrases to create continuity
        self.follow_ups = [
            "Building on that,",
            "Related to what you mentioned,",
            "That makes me think about",
            "That connects to",
            "This brings up another point -",
            "Following that logic,"
        ]
        
        # Phrases for acknowledging emotions/reactions
        self.emotional_acknowledgments = {
            "frustration": [
                "I notice this seems frustrating.",
                "It can be challenging when facing this kind of resistance.",
                "That resistance would test anyone's patience."
            ],
            "uncertainty": [
                "It's normal to feel uncertain in these situations.",
                "These interactions can definitely make you question your approach.",
                "Many students find this ambiguity challenging."
            ],
            "determination": [
                "I appreciate your persistence here.",
                "That determination will serve you well in real clinical settings.",
                "It's good to see you staying focused despite the obstacles."
            ]
        }
        
        # Natural speech patterns - contractions and informal phrases
        self.speech_naturalizers = {
            "I am": "I'm",
            "you are": "you're",
            "we are": "we're",
            "they are": "they're",
            "it is": "it's",
            "that is": "that's",
            "there is": "there's",
            "is not": "isn't",
            "are not": "aren't",
            "do not": "don't",
            "does not": "doesn't",
            "did not": "didn't",
            "have not": "haven't",
            "has not": "hasn't",
            "had not": "hadn't",
            "would not": "wouldn't",
            "could not": "couldn't",
            "should not": "shouldn't",
            "will not": "won't"
        }
    
    def get_section_content(self, section_name):
        """
        Get the content for a specific section of the instructor script.
        
        Args:
            section_name: Name of the section to retrieve
            
        Returns:
            List of text content from that section
        """
        if section_name in self.sections:
            return self.sections[section_name]
        else:
            return ["I don't have specific guidance on that topic, but let's think it through together."]
    
    def create_natural_response(self, base_content, mode="prebrief", previous_input=None):
        """
        Create a natural, conversational response from the script content.
        
        Args:
            base_content: The raw script content to convert to natural speech
            mode: "prebrief" or "debrief" to adjust tone accordingly
            previous_input: The student's previous input for context
            
        Returns:
            A natural-sounding instructor response
        """
        # Start with the base content
        if isinstance(base_content, list):
            # Join multi-part content, but avoid bullet points
            content = " ".join(base_content)
        else:
            content = base_content
            
        # Add a personalized opener occasionally
        if random.random() < 0.3 and previous_input:
            words = previous_input.split()
            if len(words) > 5:
                # Extract a snippet to reference
                start_idx = random.randint(0, min(10, len(words) - 3))
                snippet_length = min(random.randint(3, 6), len(words) - start_idx)
                snippet = " ".join(words[start_idx:start_idx + snippet_length])
                
                personal_openers = [
                    f"When you mentioned '{snippet}', that's an important point. ",
                    f"Your comment about '{snippet}' is quite insightful. ",
                    f"I'm glad you brought up '{snippet}'. "
                ]
                content = random.choice(personal_openers) + content
        
        # Add emotional acknowledgment in debrief mode
        if mode == "debrief" and self.observed_emotions and random.random() < 0.4:
            emotion = random.choice(list(self.observed_emotions))
            if emotion in self.emotional_acknowledgments:
                acknowledgment = random.choice(self.emotional_acknowledgments[emotion])
                
                # Insert it naturally into the content
                sentences = sent_tokenize(content)
                if len(sentences) > 2:
                    insert_point = random.randint(0, min(2, len(sentences)-1))
                    sentences.insert(insert_point, acknowledgment)
                    content = " ".join(sentences)
                else:
                    content = acknowledgment + " " + content
        
        # Apply speech naturalizers (contractions, etc.)
        for formal, natural in self.speech_naturalizers.items():
            content = re.sub(r'\b' + formal + r'\b', natural, content, flags=re.IGNORECASE)
        
        # Remove excessive structure that might be in the original script
        content = re.sub(r'\b\d+\.\s+', '', content)  # Remove numbered lists
        content = re.sub(r'•\s+', '', content)  # Remove bullet points
        
        # Add appropriate variation in sentence structures
        sentences = sent_tokenize(content)
        if len(sentences) > 3:
            # Combine some short sentences for better flow
            i = 0
            while i < len(sentences) - 1:
                if (len(sentences[i].split()) < 8 and 
                    len(sentences[i+1].split()) < 8 and
                    random.random() < 0.4):
                    
                    # Combine with an appropriate conjunction
                    conjunctions = ["and", "also", "plus", "moreover", "what's more"]
                    sentences[i] = sentences[i].rstrip('.') + ", " + random.choice(conjunctions) + " " + sentences[i+1].lower()
                    sentences.pop(i+1)
                else:
                    i += 1
            
            # Reorder some sentences for natural variation (but keep intro sentence first)
            if len(sentences) > 3:
                first_sentence = sentences[0]
                middle_sentences = sentences[1:-1]
                last_sentence = sentences[-1]
                
                # Only shuffle the middle to maintain coherence
                random.shuffle(middle_sentences)
                sentences = [first_sentence] + middle_sentences + [last_sentence]
        
        # Rebuild the content with our modifications
        content = " ".join(sentences)
        
        # Add personal touches based on mode
        if mode == "prebrief":
            # More encouraging, forward-looking language
            personal_touches = [
                " Remember, this is a learning experience.",
                " I'm confident you'll handle this well.",
                " Don't worry if things get challenging - that's part of the process.",
                " This is about practice, not perfection."
            ]
        else:  # debrief
            # More reflective, analytical language
            personal_touches = [
                " What do you think about that?",
                " I'd love to hear your thoughts on this.",
                " How does that resonate with your experience in the simulation?",
                " Does that observation feel accurate to you?"
            ]
            
        # 30% chance to add a personal touch
        if random.random() < 0.3:
            content += random.choice(personal_touches)
            
        return content
    
    def generate_prebrief_response(self, section_name=None):
        """
        Generate a natural prebrief response for the specified section.
        
        Args:
            section_name: Optional section name to focus on
            
        Returns:
            Natural conversational response from the instructor
        """
        if not section_name:
            # If no section specified, choose based on progress
            if not self.sections_covered:
                section_name = "introduction"
            elif len(self.sections_covered) < 3:
                # Choose a section we haven't covered yet
                available_sections = [s for s in self.sections.keys() 
                                     if s not in self.sections_covered 
                                     and s != "closing"]
                if available_sections:
                    section_name = random.choice(available_sections)
                else:
                    section_name = "closing"
            else:
                section_name = "closing"
                
        # Mark this section as covered
        self.sections_covered.add(section_name)
        self.current_section = section_name
        
        # Get the content and create a natural response
        content = self.get_section_content(section_name)
        return self.create_natural_response(content, mode="prebrief")
    
    def generate_debrief_response(self, section_name=None, student_input=None):
        """
        Generate a natural debrief response, potentially in response to student input.
        
        Args:
            section_name: Optional section name to focus on
            student_input: The student's previous input to respond to
            
        Returns:
            Natural conversational response from the instructor
        """
        # Update our trackers if we have student input
        if student_input:
            self.conversation_depth += 1
            
            # Store a key phrase for callbacks
            words = student_input.split()
            if len(words) > 5:
                phrase_length = min(random.randint(3, 6), len(words) - 1)
                start_idx = random.randint(0, len(words) - phrase_length)
                key_phrase = " ".join(words[start_idx:start_idx + phrase_length])
                self.student_key_phrases.append(key_phrase)
                
                # Keep the list manageable
                if len(self.student_key_phrases) > 5:
                    self.student_key_phrases.pop(0)
            
            # Simple emotion detection (would be more sophisticated in real implementation)
            frustration_words = ["frustrating", "annoyed", "difficult", "hard", "challenging"]
            uncertainty_words = ["unsure", "uncertain", "confused", "don't know", "unclear"]
            determination_words = ["determined", "committed", "focused", "persistence", "tried"]
            
            lower_input = student_input.lower()
            
            if any(word in lower_input for word in frustration_words):
                self.observed_emotions.add("frustration")
            if any(word in lower_input for word in uncertainty_words):
                self.observed_emotions.add("uncertainty")
            if any(word in lower_input for word in determination_words):
                self.observed_emotions.add("determination")
        
        if not section_name:
            # If no section specified, choose based on progress
            if not self.sections_covered:
                section_name = "introduction"
            elif len(self.sections_covered) < len(self.sections) - 1:
                # Choose a section we haven't covered yet
                available_sections = [s for s in self.sections.keys() 
                                     if s not in self.sections_covered 
                                     and s != "closing"]
                if available_sections:
                    section_name = random.choice(available_sections)
                else:
                    section_name = "closing"
            else:
                section_name = "closing"
                
        # Mark this section as covered
        self.sections_covered.add(section_name)
        self.current_section = section_name
        
        # Get the content and create a natural response
        content = self.get_section_content(section_name)
        return self.create_natural_response(content, mode="debrief", previous_input=student_input)
        
    def process_student_input(self, student_input, mode="debrief"):
        """
        Process student input and generate an appropriate response.
        
        Args:
            student_input: Text input from the student
            mode: "prebrief" or "debrief"
            
        Returns:
            Natural conversational response from the instructor
        """
        # Simple keyword matching to determine appropriate section to respond with
        
        # Keywords that might indicate the student is asking about specific topics
        keywords = {
            "objective": "objectives",
            "goal": "objectives",
            "purpose": "objectives",
            "background": "scenario_background",
            "context": "scenario_background",
            "scenario": "scenario_background",
            "sam": "character_profile",
            "character": "character_profile",
            "manager": "character_profile",
            "prepare": "preparation_tips",
            "tips": "preparation_tips",
            "advice": "preparation_tips",
            "strategy": "preparation_tips"
        }
        
        # Check for keywords in student input
        matching_sections = []
        lower_input = student_input.lower()
        
        for keyword, section in keywords.items():
            if keyword in lower_input:
                matching_sections.append(section)
        
        # Get a unique set of matching sections
        matching_sections = list(set(matching_sections))
        
        if matching_sections:
            # Respond to a specific question
            section = random.choice(matching_sections)
            if mode == "prebrief":
                return self.generate_prebrief_response(section)
            else:
                return self.generate_debrief_response(section, student_input)
        else:
            # If this is a follow-up in an ongoing conversation
            if self.conversation_depth > 0 and random.random() < 0.3 and self.student_key_phrases:
                # Reference something they said earlier
                key_phrase = random.choice(self.student_key_phrases)
                follow_up = random.choice(self.follow_ups)
                
                if mode == "prebrief":
                    response = f"{follow_up} when you mentioned '{key_phrase}', " + self.generate_prebrief_response()
                else:
                    response = f"{follow_up} when you mentioned '{key_phrase}', " + self.generate_debrief_response(student_input=student_input)
                    
                return response
            else:
                # Standard response progression
                if mode == "prebrief":
                    return self.generate_prebrief_response()
                else:
                    return self.generate_debrief_response(student_input=student_input)