#!/usr/bin/env python
import streamlit as st
import base64
import requests
import sys
import numpy as np
import pandas as pd
import openai
import uuid
import os
from models.functions import chunk, postprocess_text, process_fairy_tales_dataset, get_audio, get_images_tale
from models.classes import Example, GPT, FairyTaleGenerator


titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytail Generation')

# r = requests.post(url='https://hf.space/embed/valhalla/glide-text2im/+/api/predict/',      json={"data": ['text']})
# encoding = r.json()['data'][0][22:]
# image_64_decode = base64.b64decode(encoding)
# st.image(image_64_decode)

try:
    form_0 = st.form(key='my-form0')
    key_0 = form_0.text_input('API Key for OpenAI')
    submit_0 = form_0.form_submit_button('Submit')

except Exception as e:
    st.success(f'Need key to proceed')
try:
    form_3 = st.form(key='my-form3')
    key_3 = form_3.text_input('API Key for Play.ht')
    submit_3 = form_3.form_submit_button('Submit')

except Exception as e:
    st.success(f'Need key to proceed')
try:
    form_1 = st.form(key='my-form1')
    command = form_1.selectbox("Choose your story character",
('Knight','Princess', 'Dragon', 'Dog', 'King'))
    command_1 = form_1.selectbox("Choose your story teller",
('Woman','Man'))
    submit = form_1.form_submit_button('Generate fairytail')
    if submit:
        ftg = FairyTaleGenerator(key_0, "tales.csv")
        responce = ftg.get_one_tale(command.lower())
        image_names, parts = get_images_tale(responce, command)
        table = st.columns(len(image_names))
        for i, n in enumerate(image_names):
            table[i] = st.image(n)
        st.text_area('Fairytail about {}:'.format(command), responce)
        st.download_button('Download text of fairytail', responce)
        #responce = 'Fairytail about {}:. Tell me fairy tail'.format(command)
        #st.download_button('Download text of fairytail', command)
        if command_1 == 'Woman':
            title = "tale"
            voice = "Emilia"
            status, filename = get_audio(responce, voice, title, key_3)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)
        if command_1 == 'Man':
            title = "tale"
            voice = "Noah"
            status, filename = get_audio(responce, voice, title, key_3)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)

except Exception as e:
    st.success(f'Something Went Wrong! {e}')   
    #submit_1 = form_1.form_submit_button('Submit 1')
    #if submit_1:
        #print(responce)




