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
import random
from models.functions import chunk, postprocess_text, process_fairy_tales_dataset, \
     get_audio, get_images_tale, create_pdf, read_voices
from models.classes import Example, GPT, FairyTaleGenerator
from prompts import var_dict
#import pdfkit


#titles, stories, df = process_fairy_tales_dataset('./', 'merged_clean2.txt')
st.title('Fairytale Generation')
st.image("https://i.postimg.cc/yN20YX4F/Stories.png", use_column_width=True)

try:
    #print(st.__installation_id__)
    form_1 = st.form(key='my-form1')
    #key_openai, key_playht = read_keys()
    key_openai, key_playht = os.environ['KEY_OP'], os.environ['KEY_PLAY']
    voice_ids, voice_names = read_voices()
    hero = form_1.selectbox("Choose your story character", ('Knight', 'Princess', 'Dragon', 'Dog', 'King'))

    print('responce' in st.session_state)
    if 'responce' in st.session_state:

        responce = st.session_state['responce']
        responce = form_1.text_area('Fairytail about {}:'.format(st.session_state['story_prompt']), responce, height=400)
        show_listen = False
        print(responce)
    else:
        responce = ""
        show_listen = False


    generate = form_1.form_submit_button('Generate fairytale')
    #if 'firsttime' not in st.session_state:
    #        voice_name = form_1.selectbox("Choose your story teller", voice_names, index=62)
    #        st.session_state['firsttime'] = 1
    #else:
    voice_name = form_1.selectbox("Choose your story teller", voice_names)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
            listen = st.button('Listen fairytale', disabled=show_listen)
    with col2:
            make_images = st.button('Make images', disabled = show_listen)
    if generate:
        ftg = FairyTaleGenerator(key_openai, "tales.csv")
        st.session_state['story_prompt'] = story_prompt = random.choice(var_dict[hero])
        st.session_state['responce'] = ftg.get_one_tale(story_prompt).replace("output:", "").strip()
#             "The kingdom of Ayland was in turmoil. The king and queen had died, leaving behind them a young daughter, Princess Aurora. Aurora was only six years old when her parents\
# died, and so the kingdom was left in the care of her uncle, Duke Henry.\
# Duke Henry was a kind man, and he loved his niece dearly. But he was also\
# a ambitious man, and he had his sights set on the throne. So when it became clear that the people of Ayland would not accept him as their king, he\
# hatched a plan to get rid of Princess Aurora.\
# He had a tower built in the middle of the forest, and he had Aurora locked away inside it. The only person\
# who was allowed to visit her was her nurse, who brought her food and supplies.\
# Phillip returned the next day with a ladder. He climbed up to the window and helped Aurora down.\
# They rode off into the sunset, and they lived happily ever after.\
# "
        print("generate")
        responce = st.session_state['responce']

        print('story prompt: ', story_prompt)

        for key in ['image_names', 'audio', 'tale_parts']:
            if key in st.session_state:
                st.session_state.pop(key)
        print(responce)
        print('responce' in st.session_state)
        st.experimental_rerun()

    if make_images:
        image_names, parts = get_images_tale(responce, hero)
        st.session_state['image_names'], st.session_state['tale_parts'] = image_names, parts
        #parts = get_images_tale(responce, command)

    if 'image_names' in st.session_state:
        table = st.columns(len(st.session_state['image_names']))
        for i in range(len(st.session_state['image_names'])):
            with table[i]:
                st.image(st.session_state['image_names'][i])
    if ('image_names' in  st.session_state) and ('responce' in  st.session_state) and ('tale_parts' in st.session_state) :
        data = create_pdf(st.session_state['story_prompt'], st.session_state['tale_parts'], st.session_state['image_names'])
        st.download_button(
            "⬇️ Download Tale",
            data=data,
            file_name="tale.pdf",
            mime="application/octet-stream",
        )
        print("pdf")
    else:
        print("no pdf")
    if listen:
        index = voice_names.index(voice_name)
        voice_id = voice_ids[index]
        title = hero
        status, filename = get_audio(responce, voice_id, title, key_playht)
        print(status, filename)
        if status == 0:
            st.session_state['audio'] = filename
        else:
            st.text(f"audio for {voice_name} wasn't created by Play.ht")
    if 'audio' in st.session_state:
        form_1.audio(st.session_state['audio'] )


except Exception as e:
    st.success(f'Something Went Wrong! {e}')   





