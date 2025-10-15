import json
import os
from pathlib import Path

from dotenv import load_dotenv

from meta.singleton import SingletonMeta

load_dotenv()


class Settings(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        self.app_id = int(os.getenv("APP_ID"))
        self.install_id = int(os.getenv("INSTALL_ID"))
        self.private_key = os.getenv("PRIVATE_KEY_B64")
        self.problems_repo = os.getenv("PROBLEMS_REPO")
        self.problems_branch = os.getenv("PROBLEMS_BRANCH")
        self.solutions_repo = os.getenv("SOLUTIONS_REPO")
        self.solutions_branch = os.getenv("SOLUTIONS_BRANCH")

        # for feedback on PRs
        self.github_repo = os.getenv("GITHUB_REPOSITORY")
        # self.pr_number = os.getenv("PR_NUMBER")  # for debug only, uncomment below

        event_path = os.getenv("GITHUB_EVENT_PATH")
        if event_path and Path(event_path).exists():
            try:
                with Path.open(event_path, "r") as f:
                    event = json.load(f)
                self.pr_number = event.get("pull_request", {}).get("number")
            except Exception as e:
                print(f"⚠️ Warning: Could not read event file ({event_path}): {e}")
        else:
            print("⚠️ No GITHUB_EVENT_PATH found — running in local/test mode.")
