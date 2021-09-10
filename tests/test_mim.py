import unittest

from main import config_app


class MimTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._mim_app = config_app()

    def test_get_command(self):
        pass
        # command_text = Navi
        # self._mim_app.get_command()


if __name__ == '__main__':
    unittest.main()
