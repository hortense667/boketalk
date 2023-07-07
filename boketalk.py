import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese／日本語でお願いします' if target_language == 'ja' else 'English'}:\n{text}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

def generate_joke(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create a ironical joke based on this text:\n{text}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

st.title("TOKYO Boke Talk ／ 東京ボケトーク")
text = st.text_input("Enter some text")
if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language)
        joke = generate_joke(text)
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
if st.button("Clear"):
    text = ""
    st.empty()
