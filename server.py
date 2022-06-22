#!/usr/bin/env python
import streamlit as st
import sys
import numpy as np
import pandas as pd
import openai
import uuid
import os
from models.functions import chunk, postprocess_text, process_fairy_tales_dataset
from models.classes import Example, GPT, FairyTaleGenerator


titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytail Generation')
st.image("https://i.postimg.cc/yN20YX4F/Stories.png", use_column_width=True)
#keywords = ['Princess stuck in tower', 'Dragon and birds','Little boy, who disobey parent','Sun day','Little plant', 'Dinosaur and men']
keywords = ['Flowers and bees']

try:
    form_0 = st.form(key='my-form0')
    key = form_0.text_input('API Key for OpenAI')
    submit_0 = form_0.form_submit_button('Submit')

except Exception as e:
    st.success(f'Need key to proceed')
try:
    form_1 = st.form(key='my-form1')
    command = form_1.selectbox("Choose your story character",
('knight','princess', 'dragon', 'dog', 'king'))
    submit = form_1.form_submit_button('Submit')

    if submit:
        #ftg = FairyTaleGenerator(key, "tales.csv")
        #responce = ftg.get_one_tale(command)
        st.text_area('Fairytail about {}:'.format(command), responce)
        st.download_button('Download text of fairytail', responce)
        language = 'en'
        myobj = gTTS(text=responce, lang=language, slow=False)
        myobj.save("welcome.mp3")
        audio_file = open('welcome.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
            
except Exception as e:
    st.success(f'Something Went Wrong! {e}')


#print(f'Audio content written to file "{outfile}"')


#responce = GPT_Completion(recipe)
#st.text(responce)

