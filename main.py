import flet as ft
import requests
import streamlit as st
import base64

api_token = "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"


def query(payload, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://fawaz-nlx-gpt.hf.space/api/predict/"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def main(page: ft.Page):
    page.title = "FARI - Visual question answering"
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    question = ft.TextField(hint_text="Ask question about the image?", width=300)
    quest_label = ft.Text(value="test", color="#8f8f8f", size=20)
    
    images = ft.Row(expand=1, wrap=True, scroll="always", alignment=ft.MainAxisAlignment.CENTER)
    
    for i in range(0, 4):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/150/150?{i}",
                fit=ft.ImageFit.NONE,
                width=150,
                height=150,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(20),
            )
        )
    
    page.update()   
            
    def ask(e):
        quest_label.value = "Question: " + question.value
        question.value = ""
        question.focus()
        question.update()
        page.update()
        # Send request
    
    def takePic(e):
        image = st.camera_input("Take a picture")
        if image:
            image_data = "data:image/png;base64," +base64.b64encode(image.read()).decode('utf-8')
            print("DEBUG")
        # Run the webcam
    
    def selectPic(e):
        file_picker.pick_files(allow_multiple=True)
        upload_list = []
        if file_picker.result != None and file_picker.result.files != None:
            for f in file_picker.result.files:
                upload_list.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(upload_list)
        print(upload_list)

    page.add(
        ft.Row(
            [
                ft.Image(
                    src=f"/img/logo.png",
                    #src=f"/icons/icon-512.png",
                    width=200,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
            ],
            alignment= ft.Alignment(-2.5, -1.5)
        )
    )

    page.add(
        ft.Row(
            [
                ft.Text(value="Visual question answering", color="#2250c6", size=50)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
    page.add(
        ft.Row(
            [   
                ft.ElevatedButton("Select a picture", on_click=selectPic),
                ft.ElevatedButton("Take a picture", on_click=takePic)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [
                images,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
    page.add(
        ft.Row(
            [
                question, 
                ft.ElevatedButton("Ask", on_click=ask)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
    page.add(
        ft.Row(
            [
                quest_label,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    


ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)