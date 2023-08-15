import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language, model, temperature, region):
    translation_style = ""
    if region == "Osaka":
        translation_style = " in Osaka dialect"
    elif region == "Kyoto":
        translation_style = " in Kyoto dialect"
    elif region == "Nagoya":
        translation_style = " in Nagoya dialect"
    elif region == "Kagoshima":
        translation_style = " in Kagoshima dialect"
    elif region == "Tsugaru":
        translation_style = " in Tsugaru dialect"
    elif region == "Okinawa":
        translation_style = " in Okinawa dialect"
    # Add more dialects or regions as needed

    prompt = f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese' if target_language == 'ja' else 'English'}{translation_style}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

def generate_joke(prompt, model, temperature):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

st.title("TOKYO Boke Talk／東京ボケトーク")

st.markdown(
"""
-- ver.0.291 -- 2023/08/15 [@hortense667](https://twitter.com/hortense667)　 
"""
)

text = st.text_input("Enter some text")

# Sidebar configuration
st.sidebar.title("オプション設定")
model_options = ["gpt-4", "gpt-3.5-turbo"]
model_name = st.sidebar.radio("Select a model:", model_options)
temperature = st.sidebar.slider("Set the temperature:", 0.0, 1.0, 0.7)

joke_type_options = [
    "なにも指定しない",
    "自分で指定する",
    "funny",
    "heartwarming",
    "clean",
    "childish",
    "witty",
    "highbrow",
    "droll",
    "parody",
    "surreal or absurd",
    "dad",
    "dirty",
    "self-deprecating",
    "Potty",
]
selected_joke_type = st.sidebar.selectbox("ジョークの種類", joke_type_options)
if selected_joke_type == "自分で指定する":
    selected_joke_type = st.sidebar.text_input("Specify your type:")

region_options = [
    "Standard",
    "Osaka",
    "Kyoto",
    "Nagoya",
    "Kagoshima",
    "Tsugaru",
    "Okinawa",
]
selected_region = st.sidebar.selectbox("Select a region:", region_options)

if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language, model_name, temperature, selected_region)
        joke_prompt = f"Create a {selected_joke_type} joke based on this text:\n{text}" if selected_joke_type != "なにも指定しない" else f"Create a joke based on this text:\n{text}"
        joke = generate_joke(joke_prompt, model_name, temperature)
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")

