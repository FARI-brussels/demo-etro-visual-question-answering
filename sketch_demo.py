import streamlit as st
import pandas as pd
import numpy as np
import requests
import base64

api_token = "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"
def query(payload, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://carolineec-informativedrawings.hf.space/api/predict/"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

st.title('Sketch')


picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)
    img_string = base64.b64encode(picture.read()).decode('utf-8')
    base64_str = "data:image/png;base64," + img_string


if st.button('Submit'):
	data = {"data":[base64_str, "style 2"]}
	result = query(data, api_token)
	image = base64.b64decode(result["data"][0].split(",")[1].encode('utf-8'))
	st.image(image)






