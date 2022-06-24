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
from models.functions import chunk, postprocess_text, process_fairy_tales_dataset, \
     get_audio, get_images_tale, create_pdf, read_keys
from models.classes import Example, GPT, FairyTaleGenerator
#import pdfkit

if 'store' not in st.session_state:
     st.session_state.store = False

titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytail Generation')

# r = requests.post(url='https://hf.space/embed/valhalla/glide-text2im/+/api/predict/',      json={"data": ['text']})
# encoding = r.json()['data'][0][22:]
# image_64_decode = base64.b64decode(encoding)
# st.image(image_64_decode)

# try:
#     form_0 = st.form(key='my-form0')
#     key_0 = form_0.text_input('API Key for OpenAI')
#     submit_0 = form_0.form_submit_button('Submit')
#
# except Exception as e:
#     st.success(f'Need key to proceed')
# try:
#     form_3 = st.form(key='my-form3')
#     key_3 = form_3.text_input('API Key for Play.ht')
#     submit_3 = form_3.form_submit_button('Submit')
#
# except Exception as e:
#     st.success(f'Need key to proceed')
try:
    form_1 = st.form(key='my-form1')
    key_openai, key_playht = read_keys()
    #key_0 = form_1.text_input('API Key for OpenAI')
    #key_3 = form_1.text_input('API Key for Play.ht')
    command = form_1.selectbox("Choose your story character",
('Knight','Princess', 'Dragon', 'Dog', 'King'))
    submit = form_1.form_submit_button('Generate fairytail')
    if submit:
        #ftg = FairyTaleGenerator(key_openai, "tales.csv")
        if 'responce' not in st.session_state:
            st.session_state['responce'] = "The kingdom of Ayland was in turmoil. The king and queen had died, leaving behind them a young daughter, Princess Aurora. Aurora was only six years old when her parents\
died, and so the kingdom was left in the care of her uncle, Duke Henry.\
Duke Henry was a kind man, and he loved his niece dearly. But he was also\
a ambitious man, and he had his sights set on the throne. So when it became clear that the people of Ayland would not accept him as their king, he\
hatched a plan to get rid of Princess Aurora.\
He had a tower built in the middle of the forest, and he had Aurora locked away inside it. The only person\
who was allowed to visit her was her nurse, who brought her food and supplies.\
Phillip returned the next day with a ladder. He climbed up to the window and helped Aurora down.\
They rode off into the sunset, and they lived happily ever after.\
"
        #ftg.get_one_tale(command.lower())
        image_names, parts = get_images_tale(st.session_state['responce'], command)
        #parts = get_images_tale(responce, command)
        table = st.columns(len(image_names))
        for i, n in enumerate(image_names):
            table[i] = st.image(n)
        st.text_area('Fairytail about {}:'.format(command.lower()), st.session_state['responce'], height = 400)
        data = create_pdf(parts, image_names)
        #data = create_pdf(parts)
        if submit or st.session_state.store:
            st.session_state.store = True
        st.download_button(
            "⬇️ Download PDF",
            data=data,
            file_name="tale.pdf",
            mime="application/octet-stream",
        )
        #st.download_button('Download text of fairytail', responce)
        #responce = 'Fairytail about {}:. Tell me fairy tail'.format(command)
        #st.download_button('Download text of fairytail', command)

except Exception as e:
    st.success(f'Something Went Wrong! {e}')   
    #submit_1 = form_1.form_submit_button('Submit 1')
    #if submit_1:
        #print(responce)
try:
    form_2 = st.form(key='my-form2')
    command_2 = form_2.selectbox("Choose your story teller",
('Woman','Man'))
    submit = form_2.form_submit_button('Generate story teller voice')
    if submit:
        if command_2 == 'Woman':
            title = "tale"
            voice = "Emilia"
            status, filename = get_audio(st.session_state['responce'], voice, title, key_playht)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)
        if command_2 == 'Man':
            title = "tale"
            voice = "Noah"
            status, filename = get_audio(st.session_state['responce'], voice, title, key_playht)
            #audio_file = open('welcome.mp3', 'rb')
            #audio_bytes = audio_file.read()
            st.audio(filename)

except Exception as e:
    st.success(f'Something Went Wrong! {e}')  



