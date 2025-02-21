import streamlit as st
import time
from openai import OpenAI
import os
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in environment variables.")
    raise EnvironmentError("Missing OPENAI_API_KEY.")

client = OpenAI(api_key=OPENAI_API_KEY)

doc_dir = "docs"

st.title("RAG Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get chatbot response
def chatbot_response(user_message):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": user_message},
        ],
        stream=True,
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
            time.sleep(0.05)  # Smooth streaming effect

#Function document process
def load_and_index_documents(documents):
    filename = []
    texts = []
    for filename in os.listdir(doc_dir):
        file_path = os.path.join(doc_dir, filename)
        with open(file_path, "r") as file:
            text = file.read()
            texts.append(text)
            

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""
        response_stream = chatbot_response(prompt)
        response_container = st.empty()
        
        for word in response_stream:
            response_text += word
            response_container.markdown(response_text)  # Update dynamically

    st.session_state.messages.append({"role": "assistant", "content": response_text})