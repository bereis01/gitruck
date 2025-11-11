from src.html import Html


def test_doc_on_init():
    html = Html()

    assert html.style == (
        ".center {\n"
        "display: block;\n"
        "margin-left: auto;\n"
        "margin-right: auto;\n"
        "width: 50%;\n"
        "}\n"
    )
    assert html.body == ""


def test_add_paragraph():
    html = Html()

    html.add_paragraph("lorem ipsum")

    assert '<p style="text-align: center">lorem ipsum</p>\n' in html.body


def test_add_empty_paragraph():
    html = Html()

    html.add_paragraph("")

    assert '<p style="text-align: center"></p>\n' in html.body
