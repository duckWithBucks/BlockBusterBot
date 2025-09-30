import streamlit as st
import pandas as pd

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def generate_response(prompt: str, tone: str) -> str:
    # Example: make response style depend on tone
    if tone == "Friendly":
        return f"😊 Sure! You said: {prompt}"
    elif tone == "Formal":
        return f"Understood. You said: {prompt}"
    elif tone == "Funny":
        return f"😂 Haha, got it! You said: {prompt}"
    else:
        return f"You said: {prompt}"

def main():
    st.title("My First Chatbot")
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
    robot_img = "robot.png"  # add this image file to your project folder

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=robot_img):
                st.write(message["content"])
        else:
            with st.chat_message("user", avatar=user_emoji):
                st.write(message["content"])

    # ---------------- Chat Input ----------------
    if prompt := st.chat_input("What's on your mind?"):
        # Show user’s message
        with st.chat_message("user", avatar=user_emoji):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate bot response (using tone as an example customization)
        response = generate_response(prompt, tone)

        # Show assistant’s message
        with st.chat_message("assistant", avatar=robot_img):
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()