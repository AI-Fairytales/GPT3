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
     get_audio, get_images_tale, create_pdf, read_keys, read_voices
from models.classes import Example, GPT, FairyTaleGenerator
#import pdfkit


#titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytale Generation')


try:
    #print(st.__installation_id__)
    form_1 = st.form(key='my-form1')
    key_openai, key_playht = read_keys()
    voice_ids, voice_names = read_voices()
    hero = form_1.selectbox("Choose your story character", ('Knight', 'Princess', 'Dragon', 'Dog', 'King'))
    print('responce' in st.session_state)
    if 'responce' in st.session_state:

        responce = st.session_state['responce']
        responce = form_1.text_area('Fairytail about {}:'.format(hero), responce, height=400)
        show_listen = False
        print(responce)
    else:
        responce = ""
        show_listen = False


    generate = form_1.form_submit_button('Generate fairytale')
    voice_name = form_1.selectbox("Choose your story teller", voice_names)
    listen = st.button('Listen fairytale', disabled = show_listen)
    make_images = st.button('Make images', disabled = show_listen)
    if generate:
        #ftg = FairyTaleGenerator(key_openai, "tales.csv")
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
        print("generate")
        responce = st.session_state['responce']
        if 'image_names' in st.session_state:
                st.session_state.pop('image_names')
        if 'audio' in st.session_state:
                st.session_state.pop('audio')
        print(responce)
        print('responce' in st.session_state)

    if make_images:
        #responce = ftg.get_one_tale(command.lower())
        image_names, parts = get_images_tale(responce, hero)
        st.session_state['image_names'], st.session_state['tale_parts'] = image_names, parts
        #parts = get_images_tale(responce, command)

    if 'image_names' in st.session_state:
        table = st.columns(len(st.session_state['image_names']))
        for i, n in enumerate(st.session_state['image_names']):
            table[i] = st.image(n)
        # st.text_area('Fairytail about {}:'.format(hero), responce, height = 400)
        # data = create_pdf(parts, image_names)
        # #data = create_pdf(parts)
        # st.download_button(
        #     "⬇️ Download Tale",
        #     data=data,
        #     file_name="tale.pdf",
        #     mime="application/octet-stream",
        # )
    if listen:
        index = voice_names.index(voice_name)
        voice_id = voice_ids[index]
        title = hero
        status, filename = get_audio(responce, voice_id, title, key_playht)
        print(status, filename)
        if status == 0:
            st.session_state['audio'] = filename
    if 'audio' in st.session_state:
        form_1.audio(st.session_state['audio'] )


except Exception as e:
    st.success(f'Something Went Wrong! {e}')   





