import streamlit as st
import openai

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_to_japanese(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to Japanese:\n{text}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

def generate_joke(text):
    response = openai.Completion.create(
        engine="GPT-4",
        prompt=f"Create a bad joke based on this text:\n{text}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

st.title("TOKYO Boke Talk／東京ボケトーク")
text = st.text_input("Enter some text (in English)")
if st.button("Translate and Generate Joke"):
    if text:
        translation = translate_to_japanese(text)
        joke = generate_joke(text)
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
if st.button("Clear"):
    text = ""
    st.empty()
