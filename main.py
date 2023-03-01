import flet as ft
from flet import RoundedRectangleBorder

import requests
import io
import random

import base64
import cv2 as cv
from PIL import Image

api_token = "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"
global current_pic_path, decoded_image, imageviewer, image_cam, pic_counter
pic_counter = 0
current_pic_path=""
decoded_image=""

def main(page: ft.Page):
    global current_pic_path, imageviewer
    
    def about(e):
        """Load the about page
        """
        page.go("/about")   

    def how(e):
        """Load the 'How does this AI works' page
        """
        page.go("/how")
        
    def query(payload, api_token):
        """Call the API

        Args:
            payload (json): Data to send
            api_token (string): Token to use the API

        Returns:
            json: API result
        """
        headers = {"Authorization": f"Bearer {api_token}"}
        API_URL = f"https://fawaz-nlx-gpt.hf.space/api/predict/"
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    def loadingScreen():
        """Show a loading bar when action are made in background
        """
        page.views.append(
            ft.View(
                    "/blank",
                    [
                        ft.Container(
                            margin=(150),
                            alignment=ft.alignment.center,
                            content=
                            ft.Column(
                                spacing=(40),
                                controls=[
                                    ft.ProgressRing(width=64, height=64, stroke_width = 4, color="#2250c6"), 
                                ]
                            )
                        ),
                    ],
                )
        )
        page.update()
    
    def ask(e):
        """Make a request to the API with the selected image

        Args:
            e (error): No way there is an error, trust me :)
        """
        global decoded_image, image_cam
        loadingScreen()
        try:
            image = requests.get(current_pic_path).content #Get image online
        except:
            pil_im = Image.fromarray(image_cam)
            b = io.BytesIO()
            pil_im.save(b, 'jpeg')
            im_bytes = b.getvalue()
            image = im_bytes
            
        image_data = "data:image/png;base64," + base64.b64encode(image).decode('utf-8')
            
        data = {"data":[image_data, question.value], "cleared": False, "example_id": None}
        result = query(data, api_token)
        
        image = result["data"][2].split(",")[1]#.encode('utf-8')
        decoded_image=image
        
        AI_resp_print.value= result["data"][0]         
        AI_expl_print.value = result["data"][1]
        question_print.value = question.value
        
        question.value = ""
        question.focus()
        question.update()
        page.update()
        page.go("/result")
    
    def clickOnImage(data):
        """Change the current pic path to the one selected by the user

        Args:
            data (string): Path of the selected image (URL or LOCAL)
        """
        global current_pic_path
        current_pic_path = data
        page.go("/ask")
    
    def items():
        """Add all the images on the home page

        Returns:
            list: List of Button item containing the image
        """
        global imageviewer
        items = []
        for i in range(0, 10):
            shift = random.randint(0, 10)
            btn = ft.ElevatedButton(
                    content= 
                        ft.Image(
                            src=f"https://picsum.photos/id/{(i*10)+shift}/400/400",
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
                    data = f"https://picsum.photos/id/{(i*10)+shift}/400/400",
                    on_click=lambda e: clickOnImage(e.control.data),
            )
            items.append(btn)
        return items 
            
    
    def takePic(e):
        """Take a picture of the user thanks to the webcam

        Args:
            e (error): No way there is an error, trust me :)
        """
        global current_pic_path, image_cam, pic_counter
        cam = cv.VideoCapture(0)   
        s, img = cam.read()
        if s:
            cv.imwrite("assets/img/cam"+ str(pic_counter) + ".jpg",img)
            image_cam = img
        current_pic_path = f"assets/img/cam"+ str(pic_counter) + ".jpg"
        pic_counter+=1
        page.go("/blank")
        page.go("/ask")
        page.update()
        
    def view_pop(view):
        """Change the current view

        Args:
            view (Flet view): New view
        """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    
    #===============================================================================
    # UIX & GUI DEFINITION
    #===============================================================================  
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
                    ft.Container(
                            margin=(50),
                            alignment=ft.alignment.center,
                            content=       
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Row(
                                            [
                                                ft.Text(value="\nChoose one of these pictures\n", color="#8f8f8f", size=18, font_family="Plain")
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
        if page.route == "/blank":
            page.views.append(
                ft.View(
                    "/blank",
                    [
                        ft.Container(
                            margin=(150),
                            alignment=ft.alignment.center,
                            content=
                            ft.Column(
                                spacing=(40),
                                controls=[
                                    ft.ProgressRing(width=64, height=64, stroke_width = 4, color="#2250c6"), 
                                ]
                            )
                        ),
                    ],
                )
            )
        page.update()

    #===============================================================================
    # MAIN CODE & GLOBAL VAR
    #===============================================================================    
    page.title = ""
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
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    


ft.app(target=main, port=8551, assets_dir="assets", view=ft.WEB_BROWSER)