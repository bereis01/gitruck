from src.html import Html


def test_style_config_and_empty_body_on_init():
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


def test_add_logo():
    html = Html()

    html.add_logo()

    assert "gitruck_logo.png" in html.body


def test_add_truck_factor():
    html = Html()

    html.add_truck_factor(54)

    assert "Your truck factor is..." in html.body
    assert "54" in html.body


def test_add_top_contributors():
    top_contributors = {"Bernardo": 54, "Ana": 12}
    html = Html()

    html.add_top_contributors(top_contributors)

    assert "These are the most important devs:" in html.body
    assert len(html.images) == 1
