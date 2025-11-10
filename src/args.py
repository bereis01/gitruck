import argparse


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="gitruck",
            description="Collaboration analysis tool for git repositories.",
        )

    def parse():
        return parser.parse_args()
