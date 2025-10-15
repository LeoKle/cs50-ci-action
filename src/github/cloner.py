import shutil
import subprocess
import tempfile
from pathlib import Path


class GithubRepoCloner:
    def __init__(self, token, repository, branch):
        self.tmpdir = tempfile.mkdtemp()
        self.repository = repository
        self.repo_name = repository.split("/")[-1]

        self.repo_dir = Path(self.tmpdir) / self.repo_name
        clone_url = f"https://x-access-token:{token}@github.com/{repository}.git"
        print(f"Cloning {repository} into {self.repo_dir}...")
        subprocess.run(
            ["git", "clone", "--single-branch", "-b", branch, clone_url, str(self.repo_dir)],
            check=True,
        )

        print(f"Repo cloned to: {self.repo_dir}")

    def get_repo_dir(self):
        """Return the full path of the cloned repository folder."""
        return self.repo_dir

    def __del__(self):
        if hasattr(self, "tmpdir") and Path(self.tmpdir).exists():
            print(f"Cleaning up temp directory: {self.tmpdir}")
            shutil.rmtree(self.tmpdir)
