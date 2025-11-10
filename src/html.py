import os


class Html:
    def __init__(self):
        self.doc = ""
        self.path = "./report"

    def add_paragraph(text: str):
        self.doc += f"<p>{text}</p>\n"

    def persist():
        # Arranges the repository
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            os.rmdir(self.path)
            os.makedirs(self.path)

        # Writes the html file
        doc = open(f"{self.path}/index.html", "w")
        doc.write(self.doc)
        doc.close()
