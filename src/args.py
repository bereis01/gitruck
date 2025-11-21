import argparse
import datetime


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="gitruck",
            description="Collaboration analysis tool for git repositories.",
        )
        self.parser.add_argument("repo_url")
        self.parser.add_argument(
            "-s",
            "--since",
            type=int,
            choices=[
                2008 + x for x in range(0, datetime.datetime.now().year - 2008 + 1)
            ],
        )
        self.parser.add_argument(
            "-u",
            "--until",
            type=int,
            choices=[
                2008 + x for x in range(0, datetime.datetime.now().year - 2008 + 1)
            ],
        )

    def get_url(self):
        args = self.parser.parse_args()
        return args.repo_url

    def get_time_period(self):
        args = self.parser.parse_args()
        return args.since, args.until
