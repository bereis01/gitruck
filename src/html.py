import os
import shutil
import requests
import itertools
from io import BytesIO
from matplotlib import pyplot as plt


class Html:
    def __init__(self):
        self._persist_path = "./report/"
        self._images_path = "assets/"

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

    def add_logo(self):
        self.body += (
            '<p style="margin-bottom:0px;" align="center">\n'
            '<img src="../assets/gitruck_logo.png" width="250" height="250">\n'
            "</p>"
        )

    def add_truck_factor(self, truck_factor: int):
        self.body += (
            '<p style="margin-top:0px;" align="center">'
            '<a style="font-size:40px">Your truck factor is...</a>'
            '<a style="font-size:50px;color:#F4C524;text-shadow:2px 0 #000, -2px 0 #000, 0 2px #000, 0 -2px #000,'
            f'1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000;">{truck_factor}</a>'
            "</p>"
        )

    def add_top_contributors(self, top_contributors: dict):
        # Limits the size of the list
        if len(top_contributors) > 10:
            top_contributors = dict(itertools.islice(top_contributors.items(), 10))

        # Generates the visualization
        img = BytesIO()
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 4)
        for contributor, count in list(top_contributors.items())[::-1]:
            bar = ax.barh(contributor, count, color="#F4C524")
            ax.bar_label(bar, labels=["  " + contributor], label_type="edge")
        plt.xlim(
            (0, int((4 / 3) * list(top_contributors.values())[0]))
        )  # Avoids label cropping
        ax.get_yaxis().set_ticks([])  # Hides name labels
        ax.set_xlabel("Authored Files")
        fig.savefig(img, format="png", dpi=300)
        plt.close()

        # Appends it to the buffer
        image_ID = len(self.images)
        self.images.append(img)

        # Includes it in the body of the doc
        width, height = fig.get_size_inches() * fig.dpi
        self.body += (
            '<p align="center">'
            '<a style="font-size:25px">These are the most important devs:</a></br>'
            f'<img src="./{self._images_path}{image_ID}.png" width="{width}" height="{height}">'
            "</p>"
        )

    def add_contributor_statistics(self, total: dict, positive: dict, negative: dict):
        # Generates the visualization
        img = BytesIO()
        fig, ax = plt.subplots(1, 3)
        fig.set_size_inches(12, 3.5)

        ax[0].plot(total.keys(), total.values(), color="#F4C524")
        ax[0].set_ylim(0, max(total.values()))  # Normalizes scale according to total
        ax[0].set_title("Total Amount of Contributors")
        ax[0].set_xlabel("Year")
        ax[0].set_ylabel("N° of Contributors")

        ax[1].plot(positive.keys(), positive.values(), color="#41E04E")
        ax[1].set_ylim(0, max(total.values()))  # Normalizes scale according to total
        ax[1].set_title("Net Amount of New Contributors")
        ax[1].set_xlabel("Year")
        ax[1].set_ylabel("N° of Contributors")

        ax[2].plot(negative.keys(), negative.values(), color="#E04141")
        ax[2].set_ylim(0, max(total.values()))  # Normalizes scale according to total
        ax[2].set_title("Net Amount of Lost Contributors")
        ax[2].set_xlabel("Year")
        ax[2].set_ylabel("N° of Contributors")

        fig.tight_layout()  # Makes things less tight lol
        fig.savefig(img, format="png", dpi=300)
        plt.close()

        # Appends it to the buffer
        image_ID = len(self.images)
        self.images.append(img)

        # Includes it in the body of the doc
        width, height = fig.get_size_inches() * fig.dpi
        self.body += (
            '<p style="margin-top:50px;" align="center">'
            '<a style="font-size:25px;">Here are some statistics about the amount of contributors:</a></br>'
            f'<img style="margin-top:20px;" src="./{self._images_path}{image_ID}.png" width="{width}" height="{height}">'
            "</p>"
        )

    def add_contribution_statistics(self):
        pass

    def persist(self):
        # Arranges the repository
        if not os.path.exists(self._persist_path):
            os.makedirs(self._persist_path)
        else:
            shutil.rmtree(self._persist_path)
            os.makedirs(self._persist_path)
        os.makedirs(self._persist_path + self._images_path)

        # Writes buffered images
        for image_ID in range(len(self.images)):
            image = self.images[image_ID]
            out = open(f"{self._persist_path}{self._images_path}{image_ID}.png", "wb")
            out.write(image.getbuffer())
            out.close()

        # Parses all the html components
        doc_str = "<!DOCTYPE html>\n<html>\n<head>\n<style>"
        doc_str += self.style
        doc_str += "</style>\n</head>\n<body>"
        doc_str += self.body
        doc_str += "</body>\n</html>"

        # Writes the html file
        doc_file = open(f"{self._persist_path}/index.html", "w")
        doc_file.write(doc_str)
        doc_file.close()
