import google.generativeai as genai
import json
import os

# We need to import the prompts from the utils folder.
# This line adds the parent directory (study_agent) to the Python path
# so it can find the 'utils' module.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.prompts import SYSTEM_PROMPT, RESPONSE_SCHEMA
except ImportError:
    # Handle the case where the script might be run directly for testing
    print("Warning: Could not import prompts.py. Make sure you are running from the main directory.")
    # Define fallbacks just in case
    SYSTEM_PROMPT = "You are a helpful assistant."
    RESPONSE_SCHEMA = {}


def get_study_aids(text_content):
    """
    Calls the (pre-configured) Gemini API to generate study aids.
    
    Args:
        text_content (str): The text extracted from the PDF.
        
    Returns:
        dict: A dictionary with 'topics', 'flashcards', and 'quiz'.
    """
    
    print("Initializing Gemini Model...")
    # Note: The API key should be configured in the main app.py file
    # using genai.configure(api_key=...)
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-09-2025",
        system_instruction=SYSTEM_PROMPT,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": RESPONSE_SCHEMA,
            "temperature": 0.7, # Add a bit of creativity
        }
    )
    
    # Limit text size to avoid API errors (30k chars is a safe limit)
    user_query = f"""Here is the text from the study notes:
    ---
    {text_content[:30000]} 
    ---
    Please generate the study aids based on this text."""
    
    try:
        print("Sending request to Gemini API...")
        response = model.generate_content(user_query)
        
        # Parse the JSON string from the response
        study_aids = json.loads(response.text)
        print("Successfully parsed response from Gemini.")
        return study_aids
        
    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        # Try to provide more context from the response if possible
        try:
            print(f"Gemini response prompt_feedback: {response.prompt_feedback}")
        except Exception:
            pass
        raise ValueError(f"Failed to generate/parse study aids from Gemini. Error: {e}")