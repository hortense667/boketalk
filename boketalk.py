import streamlit as st
from openai import OpenAI, models
from openai.api_resources.completion import Completion

# API key is obtained from the Streamlit secrets
openai = OpenAI(st.secrets["OPENAI_API_KEY"])

def translate_to_japanese(text):
    model = models.Text2Text("text-davinci-002")
    prompt = f"Translate the following English text to Japanese:\n{text}"
    completion = Completion.create(model=model, prompt=prompt, max_tokens=60)
    return completion.choices[0].text.strip()

def generate_joke(text):
    model = models.Text2Text("text-davinci-002")
    prompt = f"Create a joke based on this text:\n{text}"
    completion = Completion.create(model=model, prompt=prompt, max_tokens=60)
    return completion.choices[0].text.strip()

st.title("OpenAI Translation and Joke Generator")
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
