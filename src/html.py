import os
import shutil
from io import BytesIO


class Html:
    def __init__(self):
        self.logo = (
            '<p align="center">\n'
            '<img src="../assets/gitruck_logo.png" width="250" height="250">\n'
            "</p>"
        )
        self.style = (
            ".center {\n"
            "display: block;\n"
            "margin-left: auto;\n"
            "margin-right: auto;\n"
            "width: 50%;\n"
            "}\n"
        )
        self.body = ""

        self.images = []

        self.path = "./report"
        self.images_path = "/assets"

    def add_paragraph(self, text: str):
        self.body += f'<p style="text-align: center">{text}</p>\n'

    def add_image(self, image: BytesIO):
        image_ID = len(self.images)
        self.images.append(image)

        self.body += (
            "<img "
            f'src=".{self.images_path}/{image_ID}.png" '
            'style="width:400px;height:300px;" '
            'class="center" '
            ">\n"
        )

    def add_truck_factor(self, truck_factor: int):
        self.body += (
            '<p align="center">'
            '<a style="font-size:40px">Your truck factor is...</a>'
            '<a style="font-size:50px;color:yellow;text-shadow:2px 0 #000, -2px 0 #000, 0 2px #000, 0 -2px #000,'
            f'1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000;">{truck_factor}</a>'
            "</p>"
        )

    def add_most_important_devs(self, image: BytesIO):
        image_ID = len(self.images)
        self.images.append(image)

        self.body += (
            '<p align="center">'
            '<a style="font-size:25px">These are the most important devs:</a></br>'
            f'<img src=".{self.images_path}/{image_ID}.png" width="400" height="400">'
            "</p>"
        )

    def persist(self):
        # Arranges the repository
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            shutil.rmtree(self.path)
            os.makedirs(self.path)

        os.makedirs(self.path + self.images_path)

        # Writes buffered images
        for image_ID in range(len(self.images)):
            image = self.images[image_ID]
            out = open(f"{self.path}{self.images_path}/{image_ID}.png", "wb")
            out.write(image.getbuffer())
            out.close()

        # Parses all the html components
        doc_str = "<!DOCTYPE html>\n<html>\n<head>\n<style>"
        doc_str += self.style
        doc_str += "</style>\n</head>\n<body>"
        doc_str += self.logo
        doc_str += self.body
        doc_str += "</body>\n</html>"

        # Writes the html file
        doc_file = open(f"{self.path}/index.html", "w")
        doc_file.write(doc_str)
        doc_file.close()
