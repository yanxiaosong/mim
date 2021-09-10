import unittest

from mim.ui import SimpleMimUI


class UITestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._ui = SimpleMimUI()

    def test_output(self):

        output_text = 'This is a test.'
        self.assertEqual(self._ui.output_text(output_text), output_text)

        output_text = 'This is a test.'
        start_pos = 0
        end_pos = len(output_text)
        self.assertEqual(self._ui.output_text(output_text, start_pos, end_pos),
                         "[This is a test.]")

        output_text = 'This is a test.'
        start_pos = 3
        end_pos = 6
        self.assertEqual(self._ui.output_text(output_text, start_pos, end_pos),
                         "Thi[s i]s a test.")

        output_text = 'This is a test.'
        start_pos = 3
        end_pos = 4
        self.assertEqual(self._ui.output_text(output_text, start_pos, end_pos),
                         "Thi[s] is a test.")

        output_text = 'This is a test.'
        start_pos = len(output_text) - 1
        end_pos = len(output_text)
        self.assertEqual(self._ui.output_text(output_text, start_pos, end_pos),
                         "This is a test[.]")

        output_text = 'This is a test.'
        start_pos = 4
        end_pos = 4
        self.assertEqual(self._ui.output_text(output_text, start_pos, end_pos),
                         "This is a test.")


if __name__ == '__main__':
    unittest.main()
