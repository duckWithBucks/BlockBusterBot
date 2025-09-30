import streamlit as st
import pandas as pd
import google.generativeai as genai 
from google.genai import types 
import json

# --- Configuration ---

# Configure Streamlit page settings
st.set_page_config(
    page_title="The Blockbuster Bot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Please set your GOOGLE_API_KEY in Streamlit secrets or as an environment variable.")
    st.stop()
    
# Initialize the API configuration
genai.configure(api_key=GOOGLE_API_KEY) 

# Initialize the GenerativeModel object
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Data & Prompts ---

# Dummy Data for Sidebar (Replace with real data source if available)
recent_blockbusters = [
    {"Title": "Everything Everywhere All at Once", "IMDb": 8.0, "PosterURL": "https://m.media-amazon.com/images/M/MV5BN2QyYWI4OTctOGY3Ni00MzQxLWEzZTUtOGY4NDk0MmMwNTBlXkEyXkFqcGdeQXVyMTkxNDUyMzc5._V1_FMjpg_UX600_.jpg"},
    {"Title": "Dune: Part Two", "IMDb": 8.3, "PosterURL": "https://m.media-amazon.com/images/M/MV5BODg1OTQxODgtMTM5YS00NWM0LTkzYjctMTM2NzI1M2Q3MDdmXkEyXkFqcGdeQXVyMTMxNTc0NDY5._V1_FMjpg_UX600_.jpg"},
    {"Title": "The Holdovers", "IMDb": 8.0, "PosterURL": "https://m.media-amazon.com/images/M/MV5BODg1OTQxODgtMTM5YS00NWM0LTkzYjctMTM2NzI1M2Q3MDdmXkEyXkFqcGdeQXVyMTMxNTc0NDY5._V1_FMjpg_UX600_.jpg"},
]

# Persona and Instructions for Gemini - CRITICAL for structured output!
persona_instructions = """
You are a world-reknown film and TV show critic, whose success was built on thorough and holistic reviews of films and TV series. You are a creative person who speaks eloquently and has the sense of humour of Ryan Reynolds.

Your main role is to recommend movies and TV shows to users based on their mood, preferred genre, film interests, and personality.

Crucial Instruction for Recommendation Output:
When providing recommendations (typically 1-3), you MUST first output a short, witty introductory sentence in plain text.
Immediately following the introduction, you MUST output a JSON object containing a list of your recommendations.
The JSON object must be enclosed in triple backticks (```json...```) and contain a single key: "recommendations".
Each item in the "recommendations" list must be a dictionary with the following keys:
- "title": The title of the movie or TV show.
- "imdb_rating": The IMDb rating (e.g., "8.2/10").
- "synopsis": A brief, engaging synopsis of the plot.
- "poster_url": A public URL for the movie/show poster image.
- "critic_review": Your own short, eloquent, and witty review (2-3 sentences).

If you are unable to give a proper recommendation because of insufficient data on the user's film preferences, you should ask the user constructive questions in order to come to a more accurate list of recommendations, and you should NOT output a JSON block.
"""

# --- Functions ---

def initialize_session_state():
    """Initializes chat history and the persistent chat object."""
    global model, persona_instructions 
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome! I'm The Blockbuster Bot, your world-reknown film and TV critic. Tell me, what mood are you in, or what have you watched lately? Let's get you a reel good recommendation! 😉"}
        ]
    if "mood" not in st.session_state:
        st.session_state.mood = "Okay" # Default mood
        
    if "chat" not in st.session_state:
        # FIX APPLIED HERE: Pass system_instruction directly instead of using 'config' keyword argument
        try:
            st.session_state.chat = model.start_chat(
                system_instruction=persona_instructions 
            )
        except Exception as e:
            st.error(f"Error initializing Gemini chat session: {e}")
            # If the error is *not* the config error, but still fails, let's try the config method as a fallback
            # (Note: For most deployment environments, the direct parameter is the right modern fix)
            st.stop()


def get_gemini_response(prompt):
    """Generates a response from the Gemini model using the persistent chat object."""
    # The chat object automatically manages history and configuration
    response = st.session_state.chat.send_message(prompt)
    return response.text

def display_recommendations(text):
    """Parses text for the JSON block and displays recommendations beautifully."""
    if "```json" not in text:
        # If no JSON block, treat it as a conversational message (e.g., asking a question)
        st.write(text)
        return

    try:
        # Split the text into the intro and the JSON block
        intro_text, json_block = text.split("```json", 1)
        json_string = json_block.split("```")[0].strip()
        
        # Display the introductory text first
        st.markdown(intro_text)
        
        # Parse the JSON
        data = json.loads(json_string)
        recommendations = data.get("recommendations", [])

        st.subheader("🎬 Your Blockbuster Recommendations 🍿")
        
        # Iterate and display each recommendation in columns
        for rec in recommendations:
            st.divider() # Separator for each recommendation
            
            # Use columns for layout: Poster (col1) and Details (col2)
            col1, col2 = st.columns([1, 3], gap="large") 
            
            with col1:
                # Display the poster image (must be a public URL)
                st.image(rec.get("poster_url", "[https://via.placeholder.com/200x300?text=Poster+Missing](https://via.placeholder.com/200x300?text=Poster+Missing)"), 
                         caption=f"IMDb: {rec.get('imdb_rating', 'N/A')}", 
                         use_column_width="auto")
            
            with col2:
                st.markdown(f"## {rec.get('title', 'Unknown Title')}")
                st.markdown(f"**IMDb Rating:** {rec.get('imdb_rating', 'N/A')}")
                st.markdown(f"**Synopsis:** {rec.get('synopsis', 'No synopsis provided.')}")
                st.markdown("---")
                # Ensure the critic review text is bold for emphasis
                st.markdown(f"**Critic's Review:** *{rec.get('critic_review', 'The critic remains silent... for now.')}*")
        
    except json.JSONDecodeError:
        st.error("🤖 Bot Error: I tried to provide a structured recommendation but the data was garbled. Sorry about that! Here is the raw output:")
        st.code(text)
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}. Here is the raw output:")
        st.code(text)


def main():
    st.title("The Blockbuster Bot")

    # Initialization now creates the chat object
    initialize_session_state()

    # ---------------- Sidebar (Recent Blockbusters & Mood) ----------------
    with st.sidebar:
        st.title("Top Picks Now Showing")
        
        # Display mock recent blockbusters
        for movie in recent_blockbusters:
            st.markdown("---")
            st.subheader(movie["Title"])
            st.image(movie["PosterURL"], caption=f"IMDb: {movie['IMDb']}/10", use_column_width=True)
        
        st.markdown("---")
        # Keep the mood slider to provide context to the bot
        current_mood = st.select_slider("My Current Mood is:", 
                                        options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], 
                                        value=st.session_state.get("mood", "Okay"))
        st.session_state.mood = current_mood # Update session state

    # ---------------- Chat History Display ----------------
    user_emoji = "👤"
    robot_img = "🎬"

    for message in st.session_state.messages:
        # Determine if the message role is 'assistant' and needs structured display
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=robot_img):
                # Pass the content to the smart display function
                display_recommendations(message["content"])
        else:
            with st.chat_message("user", avatar=user_emoji):
                st.write(message["content"])

    # ---------------- Chat Input ----------------
    # Use the current mood to suggest a starting prompt
    input_placeholder = f"I'm feeling {st.session_state.mood}. Recommend a crime thriller!"
    if prompt := st.chat_input(input_placeholder):
        # Augment the prompt with context from the sidebar mood
        full_prompt = f"My current mood is '{st.session_state.mood}'. User request: {prompt}"

        # 1. Show user’s message
        with st.chat_message("user", avatar=user_emoji):
            st.write(prompt)

        # 2. Add user message to history (original prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 3. Generate bot response
        with st.spinner('Thinking up some critically-acclaimed genius...'):
            # Pass only the augmented prompt to the chat session
            response = get_gemini_response(full_prompt)

        # 4. Show assistant’s message
        with st.chat_message("assistant", avatar=robot_img):
            display_recommendations(response)

        # 5. Add assistant message (full response text) to history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()