import flet as ft
from flet import BorderSide
from flet import RoundedRectangleBorder

import requests
import streamlit as st
import base64

api_token = "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"

# flet run main.py -d

def query(payload, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://fawaz-nlx-gpt.hf.space/api/predict/"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def main(page: ft.Page):
    def about(e):
        page.go("/about")   

    def how(e):
        page.go("/how")
    
    def clickOnImage(e, url):
        print(url)
        #page.go("/ask")
    
    page.title = "FARI - Visual question answering"
    
    page.fonts = {
        "Plain": "/fonts/Plain-Regular.otf",
        "Rhetorik": "/fonts/RhetorikSerifTrial-Regular.ttf"
    }

    
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    file_picker = ft.FilePicker()
    #page.overlay.append(file_picker)
    #question = ft.TextField(hint_text="Ask question about the image?")
    #quest_label = ft.Text(value="test", color="#8f8f8f", size=20, font_family="Plain")
    
    images = ft.GridView(
        expand=1,
        runs_count=3,
        max_extent=400,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=20,
    )
    
    for i in range(0, 10):
        images.controls.append(
            ft.ElevatedButton(
                content= 
                    ft.Image(
                        src=f"https://picsum.photos/400/400?{i}",
                        fit=ft.ImageFit.COVER,
                        width=500,
                        height=500,
                        border_radius=ft.border_radius.all(20),
                    ),
                style=
                    ft.ButtonStyle(
                        color={
                            ft.MaterialState.HOVERED: ft.colors.WHITE,
                            ft.MaterialState.FOCUSED: ft.colors.BLUE,
                            ft.MaterialState.DEFAULT: ft.colors.BLACK,
                        },
                        bgcolor={ft.MaterialState.FOCUSED: ft.colors.WHITE, ft.MaterialState.DEFAULT: ft.colors.WHITE},
                        padding={ft.MaterialState.DEFAULT: 0, ft.MaterialState.HOVERED: 20},
                        overlay_color=ft.colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 1},
                        animation_duration=500,
                        shape={
                            ft.MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=20),
                        },
                    ),
                on_click=clickOnImage(None, "https://picsum.photos/400/400?"+str(i))
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

    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [   
                    ft.AppBar(
                        toolbar_height= 100,
                        leading=ft.Image(
                                    src=f"/img/logo_w.png",
                                    #src=f"/icons/icon-512.png",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                        leading_width=200,
                        ##title=ft.Text("AppBar Example"),
                        center_title=False,
                        bgcolor="#2250c6",
                        actions=[
                            ft.ElevatedButton("About FARI", on_click=about),
                            ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                            ft.ElevatedButton("How does this AI works", on_click=how),
                            ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                        ],
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                [
                                    ft.Text(value="Choose one of these pictures", color="#000000", size=16, font_family="Plain")
                                ]
                            ),
                            ft.Row(
                                [
                                    images,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [
                                    #question, 
                                    #ft.ElevatedButton("Ask", on_click=ask)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ), 
                            ft.Row(
                                [
                                    #quest_label,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ],
                    )
                ],
            )
        )
        if page.route == "/ask":
            page.views.append(
                ft.View(
                    "/ask",
                    [
                        ft.AppBar(
                            toolbar_height= 100,
                            leading=ft.Image(
                                        src=f"/img/logo_w.png",
                                        #src=f"/icons/icon-512.png",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                            leading_width=200,
                            ##title=ft.Text("AppBar Example"),
                            center_title=False,
                            bgcolor="#2250c6",
                            actions=[
                                ft.ElevatedButton("About FARI", on_click=about),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                                ft.ElevatedButton("How does this AI works", on_click=how),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                            ],
                        ),
                        ft.TextButton("Choose another picture", icon="back", on_click=lambda _: page.go("/")),
                        ft.Row(
                            [   
                                ft.ElevatedButton("Select a picture", on_click=selectPic),
                                ft.ElevatedButton("Take a picture", on_click=takePic)
                            ],
                        ),
                    ],
                )
            )
        if page.route == "/about":
            page.views.append(
                ft.View(
                    "/ask",
                    [
                        ft.AppBar(
                            toolbar_height= 100,
                            leading=ft.Image(
                                        src=f"/img/logo_w.png",
                                        #src=f"/icons/icon-512.png",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                            leading_width=200,
                            ##title=ft.Text("AppBar Example"),
                            center_title=False,
                            bgcolor="#2250c6",
                            actions=[
                                ft.ElevatedButton("About FARI", on_click=about),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                                ft.ElevatedButton("How does this AI works", on_click=how),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                            ],
                        ),
                        ft.TextButton("Back home", icon="back", on_click=lambda _: page.go("/")),
                        ft.Text(value="About FARI", color="#000000", size=20, font_family="Plain")
                    ],
                )
            )
        if page.route == "/how":
            page.views.append(
                ft.View(
                    "/ask",
                    [
                        ft.AppBar(
                            toolbar_height= 100,
                            leading=ft.Image(
                                        src=f"/img/logo_w.png",
                                        #src=f"/icons/icon-512.png",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                            leading_width=200,
                            ##title=ft.Text("AppBar Example"),
                            center_title=False,
                            bgcolor="#2250c6",
                            actions=[
                                ft.ElevatedButton("About FARI", on_click=about),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                                ft.ElevatedButton("How does this AI works", on_click=how),
                                ft.Text(value="     ", color="#2250c6", size=16, font_family="Plain"),
                            ],
                        ),
                        ft.TextButton("Back home", icon="back", on_click=lambda _: page.go("/")),
                        ft.Text(value="How does this AI works", color="#000000", size=20, font_family="Plain")
                    ],
                )
            )
        page.update()
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    


ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)