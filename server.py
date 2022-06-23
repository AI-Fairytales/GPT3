#!/usr/bin/env python
import streamlit as st
import sys
import numpy as np
import pandas as pd
import openai
import uuid
import os
from models.functions import chunk, postprocess_text, process_fairy_tales_dataset, get_audio
from models.classes import Example, GPT, FairyTaleGenerator


titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytail Generation')
st.image("https://i.postimg.cc/yN20YX4F/Stories.png", use_column_width=True)
#keywords = ['Princess stuck in tower', 'Dragon and birds','Little boy, who disobey parent','Sun day','Little plant', 'Dinosaur and men']
keywords = ['Flowers and bees']
responce = 'test'
command = ''

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
('knight','princess', 'dragon', 'dog', 'king'))
    submit = form_1.form_submit_button('Submit 0')
    if submit:
        ftg = FairyTaleGenerator(key_0, "tales.csv")
        #responce = ftg.get_one_tale(command)
        #st.text_area('Fairytail about {}:'.format(command), responce)
        #st.download_button('Download text of fairytail', responce)
        responce = 'here we are in if condition'
        st.text_area('Fairytail about {}:'.format(command), command)
        st.download_button('Download text of fairytail', command)

except Exception as e:
    st.success(f'Something Went Wrong! {e}')   
try:
    command_1 = form_1.selectbox("Choose your story teller",
('woman','man'))
    submit_1 = form_1.form_submit_button('Submit 1')
    if submit_1:
        #print(responce)
        if command_1 == 'woman':
            title = "tale"
            voice = "Emilia"
            status, filename = get_audio(responce, voice, title, key_3)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)
        if command_1 == 'man':
            title = "tale"
            voice = "Noah"
            status, filename = get_audio(responce, voice, title, key_3)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)

except Exception as e:
    st.success(f'Something Went Wrong! {e}')




