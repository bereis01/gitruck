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
