import unittest

from settings import Settings


class TestSettings(unittest.TestCase):
    def test_cloner(self):
        settings1 = Settings()
        settings2 = Settings()

        self.assertEqual(id(settings1), id(settings2))
