import os
import requests
import json
import time
import pandas as pd
import random
import base64
import streamlit as st
import requests
import yaml


#HOST = "https://fairytales-api.herokuapp.com/api/v1/"
HOST = "http://localhost:5000/api/v1/"

def read_keys():
    # Read YAML file
    print(os.getcwd())
    with open("conf.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded['userid_playht'], data_loaded['userid_amazon'], data_loaded['analyse_flag']

@st.cache
def read_voices(sound_provider):
    if sound_provider == 'Amazon':
        voices = pd.read_csv("voices_amazon.csv", sep = ";")
    else:
        voices = pd.read_csv("voices_playht.csv", sep=";")
    voice_ids = voices['voice_id'].values.tolist()
    voice_names = voices['voice_name'].values.tolist()
    return voice_ids, voice_names



def send_request(endpoint, parameters):
    print(parameters)
    resp = requests.get(
        HOST + endpoint,
        params = parameters, timeout = 60##{'tale': 'hello', 'voice': 'Emma', 'service_provider' : 'Amazon'}
    )
    print(resp.headers)
    if resp.status_code == 200:
        if resp.headers['Content-Type'] == 'application/json':
            return 0, resp.json()
        else:
            return 0, resp.content
    else:
        return -1, None
