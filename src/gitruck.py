import requests
from io import BytesIO
from matplotlib import pyplot as plt


class Gitruck:
    def __init__(self, repo: str):
        self.repo = repo

    def calculate_commit_dist():
        # Retrieves information from github api
        response = requests.get(
            "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/commits"
        )
        commits = response.json()

        # Parses it
        commit_authors = []
        commit_distribution = {}
        for commit in commits:
            author = commit["author"]["login"]
            commit_authors.append(author)
            if author not in commit_distribution.keys():
                commit_distribution[author] = 1
            else:
                commit_distribution[author] += 1

        # Generates the visualization
        img = BytesIO()
        plt.hist(commit_authors)
        plt.savefig(img, format="png", dpi=300)

        return img
