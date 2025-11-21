from src.args import ArgParse


def test_cli_arguments_initialization():
    args = ArgParse()

    arguments = args.get_all_arguments()

    assert "repo_url" in arguments
    assert "since" in arguments
    assert "until" in arguments
    assert "verbose" in arguments
