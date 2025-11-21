from gitruck.html import Html


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


def test_add_contributor_statistics():
    total = {2020: 10, 2021: 15, 2022: 7}
    positive = {2020: 5, 2021: 12, 2022: 2}
    negative = {2020: 4, 2021: 3, 2022: 1}
    html = Html()

    html.add_contributor_statistics(total, positive, negative)

    assert "Here are some statistics about the amount of contributors:" in html.body
    assert len(html.images) == 1


def test_add_contribution_statistics():
    contributions = {2020: (0, 15, 7.5), 2021: (3, 7, 5), 2022: (4, 16, 10)}
    insertions = {2020: (0, 1200, 600), 2021: (300, 500, 400), 2022: (0, 100, 50)}
    deletions = {2020: (0, 300, 150), 2021: (300, 700, 500), 2022: (400, 1600, 1000)}
    html = Html()

    html.add_contribution_statistics(contributions, insertions, deletions)

    assert (
        "Here are some statistics about the characteristics of contributions:"
        in html.body
    )
    assert len(html.images) == 1
