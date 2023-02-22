import flet as ft
from flet import BorderSide
from flet import RoundedRectangleBorder

import requests
import streamlit as st
import base64

api_token = "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"
global current_pic_path
current_pic_path=""

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
        
    def ask(e):
        question_print.value = question.value
        question.value = ""
        question.focus()
        question.update()
        page.update()
        page.go("/result")
    
    def clickOnImage(e):
        global current_pic_path
        current_pic_path = e
        page.go("/ask")
    
    def items():
        items = []
        for i in range(0, 10):
            btn = ft.ElevatedButton(
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
                    data = f"https://picsum.photos/400/400?"+str(i),
                    on_click=lambda e: clickOnImage(e.control.data),
            )
            items.append(btn)
        return items
    
    
    page.title = "FARI - Visual question answering"
    page.fonts = {
        "Plain": "/fonts/Plain-Regular.otf",
        "Rhetorik": "/fonts/RhetorikSerifTrial-Regular.ttf"
    }

    

    file_picker = ft.FilePicker()
    
    question = ft.TextField(width=500, hint_text="Ask question about the image?")
    question_print = ft.TextField(width=500, hint_text="??", disabled=True)
    AI_resp_print = ft.TextField(width=500, hint_text="Yes", disabled=True)
    AI_expl_print = ft.TextField(width=500, hint_text="Because", disabled=True)
    
    
    images = ft.GridView(
        expand=1,
        runs_count=3,
        max_extent=400,
        child_aspect_ratio=1.0,
        spacing=40,
        run_spacing=40,
        controls=items(),
    )
    
    page.update()   
            
    
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
        global current_pic_path
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
                    ft.Container(
                            margin=(50),
                            alignment=ft.alignment.center,
                            content=       
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Row(
                                            [
                                                ft.Text(value="\nChoose one of these pictures\n", color="#8f8f8f", size=14, font_family="Plain")
                                            ]
                                        ),
                                        ft.Row(
                                            
                                            controls=
                                            [
                                                images,
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                )
                            
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
                        ft.Row(
                            [
                                ft.TextButton(
                                    text="Choose another picture", 
                                    icon=ft.icons.ARROW_BACK,
                                    icon_color="#2250c6",
                                    on_click=lambda _: page.go("/")
                                ),
                                
                                ft.TextButton(
                                    text="Take a picture",
                                    icon=ft.icons.CAMERA,
                                    icon_color="#2250c6",
                                    on_click=takePic
                                ),
                            ]
                        ),
                        
                        ft.Container(
                            margin=(150),
                            alignment=ft.alignment.center,
                            content=ft.Row(
                                spacing=(100),
                                controls=[
                                    ft.Image(
                                            src=current_pic_path,
                                            fit=ft.ImageFit.COVER,
                                            width=500,
                                            height=500,
                                            border_radius=ft.border_radius.all(20),
                                    ),
                                    ft.Column(
                                        spacing=(40),
                                        controls=[   
                                            ft.Text(width=500, value="Ask a question you would have regarding this image and the AI will answer your question.", color="#8f8f8f", size=20, font_family="Plain"),
                                            question,
                                            ft.ElevatedButton("Submit this question", on_click=ask, width=500)
                                        ],
                                    )
                                ],
                            )
                        )
                    ],
                )
            )
        if page.route == "/result":
            page.views.append(
                ft.View(
                    "/result",
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
                        ft.Row(
                            [
                                ft.TextButton(
                                    text="Ask another question on this image", 
                                    icon=ft.icons.ARROW_BACK,
                                    icon_color="#2250c6",
                                    on_click=lambda _: page.go("/ask")
                                ),
                            ]
                        ),
                        
                        ft.Container(
                            margin=(130),
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                spacing=(40),
                                controls=[
                                ft.Row(
                                    spacing=(100),
                                    controls=[
                                        ft.Image(
                                                src=current_pic_path,
                                                fit=ft.ImageFit.COVER,
                                                width=500,
                                                height=500,
                                                border_radius=ft.border_radius.all(20),
                                        ),
                                        ft.Column(
                                            spacing=(20),
                                            controls=[   
                                                ft.Text(value="Your question:", color="#757575", size=14, font_family="Plain"),
                                                question_print,
                                                ft.Text(value="Artificial intelligence answer:", color="#757575", size=14, font_family="Plain"),
                                                AI_resp_print,
                                                ft.Text(value="Artificial intelligence textual explanation:", color="#757575", size=14, font_family="Plain"),
                                                AI_expl_print,
                                                ft.Text(width=500,value="The highlighted area in orange on the picture are the parts of the picture the artificial intelligence used to answer your question.", color="#0075FF", size=14, font_family="Plain"),
                                                ft.ProgressRing(width=32, height=32, stroke_width = 2, color="#2250c6"), 
                                            ],
                                        )
                                    ],
                                ),
                                ft.ElevatedButton("Try again with another image", on_click=lambda _: page.go("/"), width=1120)
                                ]
                            )
                        )
                    ],
                )
            )
        if page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
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
                    "/how",
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