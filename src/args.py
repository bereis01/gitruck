import argparse


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="gitruck",
            description="Collaboration analysis tool for git repositories.",
        )
        self.parser.add_argument("repo_url")

    def get_url(self):
        args = self.parser.parse_args()
        return args.repo_url
