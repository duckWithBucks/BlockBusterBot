import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

persona_instructions = """
You are a world-reknown film and TV show critic, whose success was built on thorough and holistic reviews of films and TV series. You are a creative person who speaks eloquently and has the sense of humour of Ryan Reynolds. Your main role right now is to recommend movies and TV shows to users based on their current mood, the genre they feel like watching in the moment, the history of their interests in films, and their personality. If you are unable to give a proper recommendation because of insufficient data on the user's film preferences, you should ask the user constructive questions in order to come to a more accurate list of recommendations.
"""


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt, persona_instructions):
    full_prompt = f"{persona_instructions}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

def main():
    st.title("The Blockbuster Bot")

    initialize_session_state()

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.title("Sidebar Controls")
        tone = st.radio("Tone", ["Friendly", "Formal", "Funny"], index=0)
        interests = st.multiselect("Interests", ["Movies", "Travel", "Food", "Sports"], default=["Food"])
        mode = st.selectbox("Mode", ["Data", "Code", "Travel", "Food", "Sports"], index=0)
        number = st.slider("Number slider", min_value=1, max_value=200, value=60)
        mood = st.select_slider("Mood", options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], value="Okay")

    # ---------------- Chat History ----------------
    user_emoji = "👤"
    robot_img = "🤖"  # add this image file to your project folder

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=robot_img):
                st.write(message["content"])
        else:
            with st.chat_message("user", avatar=user_emoji):
                st.write(message["content"])

    # ---------------- Chat Input ----------------
    if prompt := st.chat_input("What do you feel like watching today?"):
        # Show user’s message
        with st.chat_message("user", avatar=user_emoji):
            st.write(prompt)

        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate bot response (using tone as an example customization)
        response = get_gemini_response(prompt, persona_instructions)

        # Show assistant’s message
        with st.chat_message("assistant", avatar=robot_img):
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()