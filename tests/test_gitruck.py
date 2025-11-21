from gitruck.gitruck import Gitruck


def test_parse_linguist_output_multiple_files():
    linguist_output = (
        "94.93%  12730      Python\n"
        "\n"
        "Python:\n"
        "  src/__main__.py\n"
        "  src/args.py"
    )
    gitruck = Gitruck()

    parsed_files = gitruck._parse_linguist_output(linguist_output)

    assert len(parsed_files) == 2
    assert "src/__main__.py" in parsed_files
    assert "src/args.py" in parsed_files


def test_parse_linguist_output_multiple_languages():
    linguist_output = (
        "94.93%  12730      Python\n"
        "5.07%   680        HTML\n"
        "\n"
        "HTML:\n"
        "  report/index.html\n"
        "\n"
        "Python:\n"
        "  src/__main__.py\n"
    )
    gitruck = Gitruck()

    parsed_files = gitruck._parse_linguist_output(linguist_output)

    assert len(parsed_files) == 2
    assert "report/index.html" in parsed_files
    assert "src/__main__.py" in parsed_files


def test_parse_linguist_output_empty_string():
    linguist_output = "\n"
    gitruck = Gitruck()

    parsed_files = gitruck._parse_linguist_output(linguist_output)

    assert len(parsed_files) == 0


def test_parse_git_contributors_output_multiple_contributors():
    git_output = (
        "\t12\tBernardo Reis de Almeida <bernardo.reis.almeida01@gmail.com>\n"
        "\t5\tBernardo Reis <92443646+bereis01@users.noreply.github.com>"
    )
    gitruck = Gitruck()

    parsed_contributors = gitruck._parse_git_contributors_output(git_output)

    assert len(parsed_contributors) == 2
    assert parsed_contributors[0] == (
        12,
        "Bernardo Reis de Almeida",
        "bernardo.reis.almeida01@gmail.com",
    )
    assert parsed_contributors[1] == (
        5,
        "Bernardo Reis",
        "92443646+bereis01@users.noreply.github.com",
    )


def test_parse_git_contributors_output_single_contributors():
    git_output = "\t12\tBernardo Reis de Almeida <bernardo.reis.almeida01@gmail.com>"
    gitruck = Gitruck()

    parsed_contributors = gitruck._parse_git_contributors_output(git_output)

    assert len(parsed_contributors) == 1
    assert parsed_contributors[0] == (
        12,
        "Bernardo Reis de Almeida",
        "bernardo.reis.almeida01@gmail.com",
    )


def test_generate_dev_names_different_devs():
    contributors = [
        (0, "Bernardo Reis", "bernardo@email.com"),
        (0, "Ana Hampton", "ana@email.com"),
    ]
    gitruck = Gitruck()

    dev_name = gitruck._generate_dev_names(contributors)

    assert len(dev_name) == 2
    assert (
        len(list(set(dev_name.values()))) == 2
    )  # Every name is mapped to a different dev


def test_generate_dev_names_same_dev_different_names_same_email():
    contributors = [
        (0, "Bernardo Reis", "bernardo@email.com"),
        (0, "Bernardo Almeida", "bernardo@email.com"),
    ]
    gitruck = Gitruck()

    dev_name = gitruck._generate_dev_names(contributors)

    assert len(dev_name) == 2
    assert (
        len(list(set(dev_name.values()))) == 1
    )  # Every name is mapped to the same dev


def test_generate_dev_names_same_dev_similar_names_different_emails():
    contributors = [
        (0, "Bernardo Reis", "bernardo@email.com"),
        (0, "BernardoReis", "notbernardo@email.com"),
    ]
    gitruck = Gitruck()

    dev_name = gitruck._generate_dev_names(contributors)

    assert len(dev_name) == 2
    assert (
        len(list(set(dev_name.values()))) == 1
    )  # Every name is mapped to the same dev


def test_normalized_DOA_results_are_in_range_0_1_for_multiple_devs():
    files = ["test.py"]
    contributors = ["Bernardo", "Ana"]
    DOA = {"Bernardo": {"test.py": 3.78}, "Ana": {"test.py": 10.24}}
    gitruck = Gitruck()

    normalized_DOA = gitruck._calculate_normalized_DOA(DOA, files, contributors)

    assert normalized_DOA["Bernardo"]["test.py"] >= 0
    assert normalized_DOA["Ana"]["test.py"] <= 1
    assert normalized_DOA["Bernardo"]["test.py"] >= 0
    assert normalized_DOA["Ana"]["test.py"] <= 1


def test_normalized_DOA_single_dev_do_not_normalize():
    files = ["test.py"]
    contributors = ["Bernardo"]
    DOA = {"Bernardo": {"test.py": 3.78}}
    gitruck = Gitruck()

    normalized_DOA = gitruck._calculate_normalized_DOA(DOA, files, contributors)

    assert normalized_DOA["Bernardo"]["test.py"] == 3.78


def test_get_log10_min_max_avg_values_for_empty_list():
    vector = []
    gitruck = Gitruck()

    result = gitruck._get_log10_min_max_avg(vector)

    assert result == (0, 0, 0)


def test_get_log10_min_max_avg_values_for_single_element():
    vector = [10]
    gitruck = Gitruck()

    result = gitruck._get_log10_min_max_avg(vector)

    assert result == (1, 1, 1)


def test_get_log10_min_max_avg_values_for_multiple_elements():
    vector = [10, 100, 1000]
    gitruck = Gitruck()

    result = gitruck._get_log10_min_max_avg(vector)

    assert result[0] == 1
    assert result[1] == 3
    assert result[2] < 3
    assert result[2] > 2


def test_get_log10_min_max_avg_values_for_zeros_vector():
    vector = [0, 0, 0]
    gitruck = Gitruck()

    result = gitruck._get_log10_min_max_avg(vector)

    assert result == (0, 0, 0)
