import os

from dotenv import load_dotenv

from meta.singleton import SingletonMeta

load_dotenv()


class Settings(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        self.app_id = os.getenv("APP_ID")
        self.install_id = os.getenv("INSTALL_ID")
        self.private_key = os.getenv("PRIVATE_KEY_B64")
        self.problems_repo = os.getenv("PROBLEMS_REPO")
        self.problems_branch = os.getenv("PROBLEMS_BRANCH")
        self.solutions_repo = os.getenv("SOLUTIONS_REPO")
        self.solutions_branch = os.getenv("SOLUTIONS_BRANCH")
