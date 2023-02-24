import flet as ft
from flet import BorderSide
from flet import RoundedRectangleBorder

import requests
import io

import base64
import cv2 as cv
from PIL import Image

api_token = "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"
global current_pic_path, decoded_image, imageviewer, image_cam
current_pic_path=""
decoded_image=""

# flet run main.py -d

def main(page: ft.Page):
    global current_pic_path
    
    def about(e):
        page.go("/about")   

    def how(e):
        page.go("/how")
        
    def query(payload, api_token): # Call API
        headers = {"Authorization": f"Bearer {api_token}"}
        API_URL = f"https://fawaz-nlx-gpt.hf.space/api/predict/"
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    def ask(e):
        global decoded_image, image_cam
        
        page.views.append(
            ft.ProgressRing(width=32, height=32, stroke_width = 2, color="#2250c6"), 
        )
        page.update()
    
        try:
            image = requests.get(current_pic_path).content #Get image online
        except:
            pil_im = Image.fromarray(image_cam)
            b = io.BytesIO()
            pil_im.save(b, 'jpeg')
            im_bytes = b.getvalue()
            image = im_bytes
        print("DEBUG:", type(image))
        image_data = "data:image/png;base64," + base64.b64encode(image).decode('utf-8')
            
        data = {"data":[image_data, question.value], "cleared": False, "example_id": None}
        result = query(data, api_token)
        
        image = result["data"][2].split(",")[1]#.encode('utf-8')
        decoded_image=image
        
        AI_resp_print. value= result["data"][0]         
        AI_expl_print.value = result["data"][1]
        question_print.value = question.value
        
        question.value = ""
        question.focus()
        question.update()
        page.update()
        page.go("/result")
    
    def clickOnImage(data):
        global current_pic_path
        current_pic_path = data
        page.go("/ask")
    
    def items():
        global imageviewer
        items = []
        for i in range(0, 10):
            btn = ft.ElevatedButton(
                    content= 
                        ft.Image(
                            src=f"https://picsum.photos/id/{i*10}/400/400",
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
                    data = f"https://picsum.photos/id/{i*10}/400/400",
                    on_click=lambda e: clickOnImage(e.control.data),
            )
            items.append(btn)
        return items
    
    
    page.title = "FARI - Visual question answering"
    page.fonts = {
        "Plain": "/fonts/Plain-Regular.otf",
        "Rhetorik": "/fonts/RhetorikSerifTrial-Regular.ttf"
    }

    
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
        global current_pic_path, imageviewer, image_cam
        cam = cv.VideoCapture(0)   
        s, img = cam.read()
        if s:
            cv.imwrite("assets/img/cam.jpg",img)
            image_cam = img
        current_pic_path = f"/img/cam.jpg"
        imageviewer = ft.Image(
            src=current_pic_path,
            fit=ft.ImageFit.COVER,
            width=500,
            height=500,
            border_radius=ft.border_radius.all(20),
        )
        page.update()
        
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    def route_change(route):
        global current_pic_path, decoded_image, imageviewer
        imageviewer = ft.Image(
            src=current_pic_path,
            fit=ft.ImageFit.COVER,
            width=500,
            height=500,
            border_radius=ft.border_radius.all(20),
        )
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [   
                    ft.AppBar(
                        toolbar_height= 100,
                        leading=ft.Image(
                                    src=f"/img/logo_w.png",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                        leading_width=200,
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
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                            leading_width=200,
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
                                    imageviewer,
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
                                                src_base64=decoded_image,
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
                                                ft.TextButton("How does it work ?", icon=ft.icons.LINK_ROUNDED, icon_color="#2250c6", on_click=lambda _: page.go('/how')),
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
                        ft.TextButton("Back home", icon=ft.icons.ARROW_BACK, icon_color="#2250c6", on_click=lambda _: page.go("/")),
                        ft.Container(
                            margin=(130),
                            alignment=ft.alignment.center,
                            content=
                            ft.Column(
                                spacing=(40),
                                controls=[
                                    ft.Text(value="We put responsible and sustainable AI research and innovation at the core of our activities.", color="#2250c6", size=35, font_family="Rhetorik", width=800),
                                    ft.Text(value="FARI is an initiative that aims to develop, study and foster the adoption and governance of AI, \nData and Robotics technologies in a trustable, transparent, open, inclusive, ethical and responsible way. \nInspired by humanistic and European values, FARI aims at helping to leverage AI-related technologies for societal benefits, \nsuch as strengthening and preserving Fundamental Human Rights and achieving United Nations' Sustainable Development Goals.",
                                    color="#757575", size=14, font_family="Plain"
                                    ),
                                    ft.TextButton("Learn more", icon=ft.icons.LINK_ROUNDED, icon_color="#2250c6", on_click=lambda _: page.launch_url('https://www.fari.brussels/institute')),
                                ]
                            )
                        ),
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
                        ft.TextButton("Back home", icon=ft.icons.ARROW_BACK, icon_color="#2250c6", on_click=lambda _: page.go("/")),
                        ft.Container(
                            margin=(110),
                            alignment=ft.alignment.center,
                            content=
                            ft.Column(
                                spacing=(40),
                                controls=[
                                    ft.Text(value="How does this AI works ?", color="#2250c6", size=35, font_family="Rhetorik", width=800),
                                    ft.Text(value="NLX-GPT: A Model for Natural Language Explanations in Vision and Vision-Language Tasks", color="#3a3a3a", size=28, font_family="Rhetorik", width=800),
                                    ft.Text(value="Fawaz Sammani1, Tanmoy Mukherjee1, Nikos Deligiannis1", color="#3a3a3a", size=14, font_family="Rhetorik", width=800),
                                    ft.Text(value="Natural language explanation (NLE) models aim at explaining the decision-making process of a black box system via generating natural language sentences which are human-friendly, high-level and fine-grained. Current NLE models1 explain the decision-making process of a vision or vision-language model (a.k.a., task model), e.g., a VQA model, via a language model (a.k.a., explanation model), e.g., GPT. Other than the additional memory resources and inference time required by the task model, the task and explanation models are completely independent, which disassociates the explanation from the reasoning process made to predict the answer. We introduce NLX-GPT, a general, compact and faithful language model that can simultaneously predict an answer and explain it. We first conduct pre-training on large scale data of image-caption pairs for general understanding of images, and then formulate the answer as a text prediction task along with the explanation. Without region proposals nor a task model, our resulting overall framework attains better evaluation scores, contains much less parameters and is 15× faster than the current SoA model. We then address the problem of evaluating the explanations which can be in many times generic, data-biased and can come in several forms. We therefore design 2 new evaluation measures: (1) explain-predict and (2) retrieval-based attack, a selfevaluation framework that requires no labels. ",
                                    color="#757575", size=14, font_family="Plain", width=800
                                    ),
                                    ft.TextButton("Learn more", icon=ft.icons.LINK_ROUNDED, icon_color="#2250c6", on_click=lambda _: page.launch_url('https://researchportal.vub.be/en/publications/nlx-gpt-a-model-for-natural-language-explanations-in-vision-and-v')),
                                ]
                            )
                        ),
                    ],
                )
            )
        page.update()
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    


ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)