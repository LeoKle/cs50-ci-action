import unittest

from settings import Settings


class TestSettings(unittest.TestCase):
    def test_cloner(self):
        args = {
            "app_id": 123,
            "install_id": 123,
            "private_key": "key",
            "problems_repo": "problems_repo",
            "solutions_repo": "solutions_repo",
        }
        settings1 = Settings(**args)
        settings2 = Settings()

        self.assertEqual(id(settings1), id(settings2))
