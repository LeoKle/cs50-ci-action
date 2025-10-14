from meta.singleton import SingletonMeta


class Settings(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        self.app_id = kwargs["app_id"]
        self.install_id = kwargs["install_id"]
        self.private_key = kwargs["private_key"]
        self.problems_repo = kwargs["problems_repo"]
        self.solutions_repo = kwargs["solutions_repo"]
