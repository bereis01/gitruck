import os
import copy
import math
import shutil
import requests
import Levenshtein
from git import Repo
from io import BytesIO


class Gitruck:
    def __init__(self):
        self._local_repository_path = "./tmp"

    def load_repository_locally(self, github_url: str):
        if os.path.exists(self._local_repository_path):
            shutil.rmtree(self._local_repository_path)
        self.conn = Repo.clone_from(self.github_url, self._local_repository_path)

    def calculate_truck_factor(self):
        files = self._get_code_file_paths()
        dev_name = self._generate_dev_names(self._get_git_contributors())
        contributors = list(set(dev_name.values()))
        commits_per_file = self._get_commits_per_file(files)

        DOA = self._calculate_DOA(files, contributors, commits_per_file, dev_name)
        normalized_DOA = self._calculate_normalized_DOA(DOA, files, contributors)

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
        top_contributors = {k: len(v) for k, v in authored_files.items()}

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

            # Recalculates superset of files
            _files = []
            for contributor in authored_files.keys():
                _files += authored_files[contributor]
            _files = list(set(_files))

        return truck_factor, top_contributors

    def _get_code_file_paths(self):
        # Uses linguist to get the files
        git_cmd = self.conn.git
        linguist_output = git_cmd.execute(["github-linguist", "-b"])

        return self._parse_linguist_output(linguist_output)

    def _parse_linguist_output(self, linguist_output: str):
        # Removes the top analysis
        raw_files = linguist_output.split("\n")
        for i in range(len(raw_files)):
            if raw_files[i] == "":
                raw_files = raw_files[i + 1 :]
                break

        # Gets the names of the files
        files = []
        for line in raw_files:
            if "  " in line:
                files.append(line.strip())

        return files

    def _get_git_contributors(self):
        # Uses the git interface to get this
        git_cmd = self.conn.git
        contributors = git_cmd.execute(["git", "shortlog", "-sne", "--all"])

        return self._parse_git_contributors_output(contributors)

    def _parse_git_contributors_output(self, contributors: str):
        contributors = contributors.split("\n")
        for i in range(len(contributors)):
            contributor = contributors[i]
            count, identifier = contributor.strip().split("\t")
            count = int(
                count
            )  # Count refers to amount of commits made by the contributor
            name, email = identifier.split("<")
            name = name.strip()
            email = email[:-1].strip()
            contributors[i] = tuple([count, name, email])
        return contributors

    def _generate_dev_names(self, contributors: list):
        # Groups names by same email
        grouped_emails = {}
        for contributor in contributors:
            if contributor[2] not in grouped_emails.keys():
                grouped_emails[contributor[2]] = [contributor[1]]
            else:
                grouped_emails[contributor[2]].append(contributor[1])

        # Unites groups of names from the previous step
        # based on their similarity
        grouped_names = []
        while len(grouped_emails.keys()) > 0:
            reference_group = grouped_emails.pop(next(iter(grouped_emails)))
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

        # Maps the names in each group
        # to a unique identifier
        dev_name = {}
        for name_group in grouped_names:
            root_name = name_group[0]
            for name in name_group:
                dev_name[name] = root_name

        return dev_name

    def _get_commits_per_file(self, files: list):
        commits_per_file = {}
        for file in files:
            commits_for_file_generator = self.conn.iter_commits(all=True, paths=file)
            commits_per_file[file] = list(commits_for_file_generator)

        return commits_per_file

    def _calculate_DOA(
        self, files: list, contributors: list, commits_per_file: dict, dev_name: dict
    ):
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
                first_author = commits_per_file[file][-1].author.name
                if (first_author in dev_name.keys()) and (
                    dev_name[commits_per_file[file][-1].author.name] == contributor
                ):
                    authorship = 1

                # Deliveries
                deliveries = 0
                acceptances = 0
                for commit in commits_per_file[file]:
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

        return DOA

    def _calculate_normalized_DOA(self, DOA: dict, files: list, contributors: list):
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
                if (max_val - min_val) != 0:
                    normalized_DOA[contributor][file] = (
                        DOA[contributor][file] - min_val
                    ) / (max_val - min_val)
                else:
                    normalized_DOA[contributor][file] = DOA[contributor][file]

        return normalized_DOA
