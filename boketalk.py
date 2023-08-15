import streamlit as st
import openai
from langdetect import detect

# API key is obtained from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_language(text):
    return detect(text)

def translate(text, target_language, model_name, temperature, region): 
    translation_styles = {
        'Standard': '',
        'Osaka': ' in 大阪弁',
        'Nagoya': ' in 名古屋弁',
        'Kagoshima': ' in 鹿児島弁',
        'Tsugaru': ' in 津軽弁'
    }
    prompt = f"Translate the following {'English' if target_language == 'ja' else 'Japanese'} text to {'Japanese' if target_language == 'ja' else 'English'}{translation_styles[region]}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def generate_joke(text, model_name, temperature, joke_type, region):
    joke_styles = {
        'Standard': '',
        'Osaka': ' in 大阪弁',
        'Nagoya': ' in 名古屋弁',
        'Kagoshima': ' in 鹿児島弁',
        'Tsugaru': ' in 津軽弁'
    }
    prompt = f"Create a {joke_type} joke based on this text{joke_styles[region]}:\n{text}" if joke_type not in ['なにも指定しない', '自分で指定する'] else f"Create a joke based on this text{joke_styles[region]}:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

st.title("TOKYO Boke Talk／東京ボケトーク")

st.markdown(
"""
-- ver.0.291 -- 2023/08/15 [@hortense667](https://twitter.com/hortense667)
"""
)

# Sidebar for options
st.sidebar.title("オプション設定")
model_name = st.sidebar.radio('言語モデル', ['gpt-4', 'gpt-3.5-turbo'])
temperature = st.sidebar.slider('創造性（Temperature）', 0.0, 1.0, 0.7)
joke_type_options = ['なにも指定しない', '自分で指定する', 'funny', 'heartworming', 'clean', 'childish', 'puzzle-like', 'witty', 'highbrow', 'droll', 'parody', 'surreal or absurd', 'dad', 'silly', 'dirty', 'self-deprecating', 'dark', 'Potty']
joke_type = st.sidebar.selectbox('ジョークの種類', joke_type_options)
region_options = ['Standard', 'Osaka', 'Nagoya', 'Kagoshima', 'Tsugaru']
region = st.sidebar.selectbox('地域オプション', region_options)

custom_joke_type = ""
if joke_type == '自分で指定する':
    custom_joke_type = st.sidebar.text_input("ジョークの種類を指定してください")

text = st.text_input("Enter some text")
if st.button("Translate and Generate Joke"):
    if text:
        target_language = 'ja' if detect_language(text) == 'en' else 'en'
        translation = translate(text, target_language, model_name, temperature, region)
        
        joke_type_to_use = custom_joke_type if joke_type == '自分で指定する' else joke_type
        joke = generate_joke(text, model_name, temperature, joke_type_to_use, region)
        
        st.write("Translation:", translation)
        st.write("Joke:", joke)
    else:
        st.write("Please enter some text.")
