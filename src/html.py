import os
import shutil


class Html:
    def __init__(self):
        self.doc = ""
        self.path = "./report"

    def add_paragraph(self, text: str):
        self.doc += f"<p>{text}</p>\n"

    def persist(self):
        # Arranges the repository
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            shutil.rmtree(self.path)
            os.makedirs(self.path)

        # Writes the html file
        doc = open(f"{self.path}/index.html", "w")
        doc.write(self.doc)
        doc.close()
