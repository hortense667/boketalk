import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language): 
    prompt =f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese／日本語でお願いします。' if target_language == 'ja' else 'English'}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def generate_joke(text): 
    prompt =f"Create a silly joke based on this text:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


st.title("TOKYO Boke Talk／東京ボケトーク")

st.markdown(
"""
-- ver.0.24 -- 2023/08/15 [@hortense667](https://twitter.com/hortense667)　 
"""
)

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
