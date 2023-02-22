import streamlit as st
import pandas as pd
import numpy as np
import requests
import base64
from PIL import Image
from io import BytesIO
from st_clickable_images import clickable_images



api_token = "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"



def query(payload, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://fawaz-nlx-gpt.hf.space/api/predict/"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

st.title('Visual question answering')


col1, col2, col3 = st.columns(3)


image=None

with col1:
    st.text('Select an image')
    images = [
            "https://cdn-icons-png.flaticon.com/512/4151/4151133.png",
            "https://historiek.net/wp-content/uploads-phistor1/2012/10/manneken-pis-560.jpg",
            "https://www.destinsparks.com/wp-content/uploads/2015/08/mountains_landscape_photography.jpg",
            "https://media.istockphoto.com/id/1331469701/photo/asian-chinese-senior-man-with-facial-hair-using-laptop-typing-working-in-office-open-plan.jpg?b=1&s=170667a&w=0&k=20&c=HsJ1LbECJslJfgXxDtV9ztseB2yDPCY87oaLbWZ3QSk=",
            "https://thumbs.dreamstime.com/b/footballer-f%C3%A9minin-alexandra-popp-dans-l-action-pendant-la-ligue-des-championnes-femmes-de-uefa-130041036.jpg",
        ]
    clicked = clickable_images(
        images,
        titles=[f"Image #{str(i)}" for i in range(4)]+ ["Take a picture with the webcam"],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
    )


with col2:
    if clicked== 0:
        image = st.camera_input("Take a picture")
        if image:
            image_data = "data:image/png;base64," +base64.b64encode(image.read()).decode('utf-8')
 

    else:
        image = requests.get(images[clicked]).content
        image_data = "data:image/png;base64," + base64.b64encode(image).decode('utf-8')
        st.image(image)

with col3:
    question = st.text_input('Ask a question', '')
    submit = st.button('Submit')

    if submit:

        data = {"data":[image_data, question], "cleared": False, "example_id": None}
        result = query(data, api_token)
        image = result["data"][2].split(",")[1].encode('utf-8')
        print(image)
        decoded_image=base64.b64decode((image))
        st.write(result["data"][0])
        st.write(result["data"][1])
        st.image(decoded_image)






