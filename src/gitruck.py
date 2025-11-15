import os
import copy
import math
import shutil
import requests
import Levenshtein
from git import Repo
from io import BytesIO
from matplotlib import pyplot as plt


class Gitruck:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.url = f"https://github.com/{owner}/{repo}.git"
        self.path = "./tmp"

    def commit_dist(self):
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
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 6)
        ax.hist(commit_authors)
        fig.savefig(img, format="png", dpi=300)
        plt.close()

        return img

    def calculate_truck_factor(self):
        # Clones repository
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        self.conn = Repo.clone_from(self.url, self.path)

        # Gets files
        # Uses linguist to get the files
        git_cmd = self.conn.git
        raw_files = git_cmd.execute(["github-linguist", "-b"])

        # Removes the top analysis
        raw_files = raw_files.split("\n")
        for i in range(len(raw_files)):
            if raw_files[i] == "":
                raw_files = raw_files[i + 1 :]
                break

        # Gets the names of the files
        _files = []
        for line in raw_files:
            if "  " in line:
                _files.append(line.strip())

        def print_files_from_git(root, files, level=0):
            for entry in root:
                if entry.type == "tree":
                    print_files_from_git(entry, files, level + 1)
                else:
                    if entry.path in _files:
                        files.append(entry)

        files = []
        print_files_from_git(self.conn.head.commit.tree, files)

        self.files = files

        # Gets contributors
        git_cmd = self.conn.git
        contributors = git_cmd.execute(["git", "shortlog", "-sne", "--all"])

        contributors = contributors.split("\n")
        for i in range(len(contributors)):
            contributor = contributors[i]
            count, identifier = contributor.strip().split("\t")
            count = int(count)
            name, email = identifier.split("<")
            name = name.strip()
            email = email[:-1].strip()
            contributors[i] = tuple([count, name, email])

        self.contributors = contributors

        # Parses contributors
        # Groups emails
        grouped_emails = {}
        for contributor in contributors:
            if contributor[2] not in grouped_emails.keys():
                grouped_emails[contributor[2]] = [contributor[1]]
            else:
                grouped_emails[contributor[2]].append(contributor[1])

        # Groups names
        grouped_names = []
        while len(grouped_emails.keys()) > 0:
            reference_group = grouped_emails.pop(list(grouped_emails.keys())[0])
            # Expands the reference group with other groups
            for key in list(grouped_emails.keys()):
                comparison_group = grouped_emails[key]
                # Checks if there is a pair of names in both groups
                # that have a Levenshtein distance of 1 or less
                for lhs_name in reference_group:
                    for rhs_name in comparison_group:
                        if Levenshtein.distance(lhs_name, rhs_name) <= 1:
                            # Unites both groups
                            reference_group += grouped_emails.pop(key)
                            break
                    else:  # Bad code to make the inner loop break propagate to the outer loop
                        continue
                    break
            grouped_names.append(reference_group)

        # Creates a mapped-dev-name
        dev_name = {}
        for name_group in grouped_names:
            root_name = name_group[0]
            for name in name_group:
                dev_name[name] = root_name

        self.dev_name = dev_name

        # Gets commits per file
        commits_per_filepath = {}
        for file in files:
            commits_for_file_generator = self.conn.iter_commits(all=True, paths=file.path)
            commits_per_filepath[file.path] = list(commits_for_file_generator)

        self.commits_per_filepath = commits_per_filepath

        # Calculates DOA and normalized DOA
        files = _files
        contributors = list(set(dev_name.values()))

        # Defines DOA data structure
        DOA = {}
        for contributor in contributors:
            DOA[contributor] = {}
            for file in files:
                DOA[contributor][file] = 0.0

        # Calculates DOA
        for contributor in contributors:
            for file in files:
                # Authorship
                authorship = 0
                first_author = commits_per_filepath[file][-1].author.name
                if (first_author in dev_name.keys()) and (
                    dev_name[commits_per_filepath[file][-1].author.name] == contributor
                ):
                    authorship = 1

                # Deliveries
                deliveries = 0
                acceptances = 0
                for commit in commits_per_filepath[file]:
                    if (commit.author.name in dev_name.keys()) and (
                        dev_name[commit.author.name] == contributor
                    ):
                        deliveries += 1
                    else:
                        acceptances += 1

                # Final value
                DOA[contributor][file] = (
                    3.293
                    + 1.098 * authorship
                    + 0.164 * deliveries
                    - 0.321 * math.log(1 + acceptances)
                )

        # Normalizes DOA
        normalized_DOA = copy.deepcopy(DOA)
        for file in files:
            # Gets minimum and maximum values
            max_val = -1
            min_val = 999999
            for contributor in contributors:
                if DOA[contributor][file] > max_val:
                    max_val = DOA[contributor][file]
                if DOA[contributor][file] < min_val:
                    min_val = DOA[contributor][file]

            # Normalizes each value
            for contributor in contributors:
                normalized_DOA[contributor][file] = (
                    DOA[contributor][file] - min_val
                ) / (max_val - min_val)

        # Calculates authored files
        # Parameters
        k = 0.75
        m = 3.293

        # Computes authored files
        authored_files = {}
        for contributor in contributors:
            authored_files[contributor] = []
            for file in files:
                if (normalized_DOA[contributor][file] >= k) and (
                    DOA[contributor][file] >= m
                ):
                    authored_files[contributor].append(file)

        # Orders it based on amount of files
        authored_files = {
            k: v
            for k, v in sorted(
                authored_files.items(), key=lambda pair: len(pair[1]), reverse=True
            )
        }

        # Calculates the truck factor
        # Calculates the superset of files
        _files = []
        for contributor in authored_files.keys():
            _files += authored_files[contributor]
        _files = list(set(_files))

        # Computes the truck factor
        truck_factor = 0
        while _files:
            # Stops if file coverage is below 50%
            if len(_files) < (0.5 * len(files)):
                break

            # Removes top author and increases truck factor
            authored_files.pop(next(iter(authored_files)), None)
            truck_factor += 1

            # Recalculates file set
            _files = []
            for contributor in authored_files.keys():
                _files += authored_files[contributor]
            _files = list(set(_files))

        return truck_factor
