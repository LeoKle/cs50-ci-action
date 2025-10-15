import unittest
from pathlib import Path

from github.cloner import GithubRepoCloner


class TestGithubRepoCloner(unittest.TestCase):
    def test_cloner(self):
        # NOTE: Public repos can be cloned with an empty token ("")
        repo = "github/.github"
        branch = "main"

        cloner = GithubRepoCloner(token="", repository=repo, branch=branch)

        repo_dir = cloner.get_repo_dir()
        self.assertTrue(Path(repo_dir).exists(), f"Repo dir does not exist: {repo_dir}")

        git_dir = Path(repo_dir) / ".git"
        self.assertTrue(git_dir.exists(), f".git directory missing in {repo_dir}")
