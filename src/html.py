import os
import shutil
from io import BytesIO


class Html:
    def __init__(self):
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
        doc_str += self.body
        doc_str += "</body>\n</html>"

        # Writes the html file
        doc_file = open(f"{self.path}/index.html", "w")
        doc_file.write(doc_str)
        doc_file.close()
