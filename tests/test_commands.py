import unittest

from mim.commands import NavigationCommand, SelectionCommand
from mim.util import TextStatus


class MimCommandTestCase(unittest.TestCase):

    def _assertions(self, text_status: TextStatus, start_pos_expected: int, end_pos_expected: int):
        text_status_updated = self.command.execute(text_status)
        self.assertEqual(text_status.current_text, text_status_updated.current_text)
        self.assertEqual(text_status.current_command, text_status_updated.current_command)
        self.assertEqual(start_pos_expected, text_status_updated.start_position)
        self.assertEqual(end_pos_expected, text_status_updated.end_position)


class NavigationTestCase(MimCommandTestCase):

    def setUp(self):
        self.command = NavigationCommand()

    def test_move_to_beginning(self):
        input_text = 'Hello World?  Hello World!'
        text_status = TextStatus(input_text, NavigationCommand.COMMAND_MOVE_TO_BEGINNING, 0, 0)

        # TEST: 'Hello World?  Hello World!'
        # EXPECTED RESULT: '[H]ello World?  Hello World!'
        text_status.start_position = 0
        text_status.end_position = 0
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

        # TEST: '[H]ello World?  Hello World!'
        # EXPECTED RESULT: '[H]ello World?  Hello World!'
        text_status.start_position = 0
        text_status.end_position = 1
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

        # TEST 'Hello W[o]rld?  Hello World!'
        # EXPECTED RESULT: '[H]ello World?  Hello World!'
        text_status.start_position = 7
        text_status.end_position = 8
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

        # TEST 'Hello World?  Hello World[!]'
        # EXPECTED RESULT: '[H]ello World?  Hello World!'
        text_status.start_position = 25
        text_status.end_position = 26
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

        # TEST 'H[ello W]orld? Hello World!'
        # EXPECTED: '[H]ello World? Hello World!'
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

    def test_move_to_end(self):
        input_text = 'Hello World?  Hello World!'
        text_status = TextStatus(input_text, NavigationCommand.COMMAND_MOVE_TO_END, 0, 0)

        last_pos = len(input_text) - 1

        # TEST: 'Hello World?  Hello World!'
        # EXPECTED RESULT: 'Hello World?  Hello World[!]'
        text_status.start_position = 0
        text_status.end_position = 0
        self._assertions(text_status, start_pos_expected=last_pos, end_pos_expected=last_pos+1)

        # TEST: '[H]ello World?  Hello World!'
        # EXPECTED RESULT: 'Hello World?  Hello World[!]'
        text_status.start_position = 0
        text_status.end_position = 1
        self._assertions(text_status, start_pos_expected=last_pos, end_pos_expected=last_pos+1)

        # TEST 'Hello W[o]rld?  Hello World!'
        # EXPECTED RESULT: 'Hello World?  Hello World[!]'
        text_status.start_position = 7
        text_status.end_position = 8
        self._assertions(text_status, start_pos_expected=last_pos, end_pos_expected=last_pos+1)

        # TEST 'Hello World?  Hello World[!]'
        # EXPECTED RESULT: 'Hello World?  Hello World[!]'
        text_status.start_position = 25
        text_status.end_position = 26
        self._assertions(text_status, start_pos_expected=last_pos, end_pos_expected=last_pos+1)

        # TEST 'H[ello W]orld?  Hello World!'
        # EXPECTED: 'Hello World?  Hello World[!]'
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=last_pos, end_pos_expected=last_pos+1)

    def test_move_to_next_matched(self):

        input_text = 'Hello World?  Hello World!'
        text_status = TextStatus(input_text, NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED, 0, 0)

        ##############################
        # search with lower case 'w'
        ##############################
        command_text = NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED + "w"
        text_status.current_command = command_text

        # TEST 'Hello World?  Hello World!'
        # EXPECTED: 'Hello[ ]World?  Hello World!'
        text_status.start_position = 0
        text_status.end_position = 0
        self._assertions(text_status, start_pos_expected=5, end_pos_expected=6)

        # TEST: 'Hello[ ]World?  Hello World!'
        # EXPECTED RESULT: 'Hello[ ]World?  Hello World!'
        text_status.start_position = 5
        text_status.end_position = 6
        self._assertions(text_status, start_pos_expected=5, end_pos_expected=6)

        # TEST 'Hello [W]orld?  Hello World!'
        # EXPECTED RESULT: 'Hello World?  Hello[ ]World!'
        text_status.start_position = 7
        text_status.end_position = 8
        self._assertions(text_status, start_pos_expected=19, end_pos_expected=20)

        # TEST 'Hello World?  Hello World[!]'
        # EXPECTED RESULT: 'Hello World?  Hello World[!]'
        text_status.start_position = 25
        text_status.end_position = 26
        self._assertions(text_status, start_pos_expected=25, end_pos_expected=26)

        # TEST 'H[ello W]orld?  Hello World!'
        # EXPECTED: 'Hello[ ]World?  Hello World!'
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=5, end_pos_expected=6)

        ##############################
        # search with upper case 'H'
        ##############################
        command_text = NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED + "H"
        text_status.current_command = command_text

        # TEST 'Hello Wor[l]d?  Hello World!'
        # EXPECTED RESULT: 'Hello World? [ ]Hello World!'
        text_status.start_position = 9
        text_status.end_position = 10
        self._assertions(text_status, start_pos_expected=13, end_pos_expected=14)

        ################################################
        # search with special characters like "!", "?"
        ################################################
        command_text = NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED + "!"
        text_status.current_command = command_text

        # TEST 'Hello Wor[l]d?  Hello World!'
        # EXPECTED RESULT: 'Hello World?  Hello Worl[d]!'
        text_status.start_position = 9
        text_status.end_position = 10
        self._assertions(text_status, start_pos_expected=24, end_pos_expected=25)

        command_text = NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED + "?"
        text_status.current_command = command_text

        # TEST 'Hello Wor[l]d?  Hello World!'
        # EXPECTED RESULT: 'Hello Worl[d]?  Hello World!'
        text_status.start_position = 9
        text_status.end_position = 10
        self._assertions(text_status, start_pos_expected=10, end_pos_expected=11)

    def test_move_to_word_end(self):

        input_text = 'Hello World?  Hello World!'
        text_status = TextStatus(input_text, NavigationCommand.COMMAND_MOVE_TO_WORD_END, 0, 0)

        # TEST 'Hello World?  Hello World!'
        # EXPECTED: 'Hell[o] World?  Hello World!'
        text_status.start_position = 0
        text_status.end_position = 0
        self._assertions(text_status, start_pos_expected=4, end_pos_expected=5)

        # TEST 'Hell[o] World?  Hello World!'
        # EXPECTED: 'Hello World[?]  Hello World!'
        text_status.start_position = 4
        text_status.end_position = 5
        self._assertions(text_status, start_pos_expected=11, end_pos_expected=12)

        # TEST 'Hello Wo[r]ld?  Hello World!'
        # EXPECTED: 'Hello World[?]  Hello World!'
        text_status.start_position = 8
        text_status.end_position = 9
        self._assertions(text_status, start_pos_expected=11, end_pos_expected=12)

        # TEST 'H[ello W]orld?  Hello World!'
        # EXPECTED: 'Hello World[?]  Hello World!'
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=11, end_pos_expected=12)

        ###################################
        # Multiple spaces between words
        ###################################
        input_text = 'Hello World?         Hello World!'
        text_status.current_text = input_text

        # TEST 'Hello World[?]         Hello World!'
        # EXPECTED: 'Hello World?         Hell[o] World!'
        text_status.start_position = 11
        text_status.end_position = 12
        self._assertions(text_status, start_pos_expected=25, end_pos_expected=26)

        #####################################
        # Trailing spaces at the end of line
        #####################################
        input_text = 'Hello World?  Hello World!        '
        text_status.current_text = input_text

        # TEST 'Hello World?  Hello World[!]        '
        # EXPECTED: 'Hello World?  Hello World[!]        '
        text_status.start_position = 25
        text_status.end_position = 26
        self._assertions(text_status, start_pos_expected=25, end_pos_expected=26)

    def test_validation(self):
        # acceptable commands
        self.assertTrue(self.command.validate('0'))
        self.assertTrue(self.command.validate('$'))
        self.assertTrue(self.command.validate('e'))
        self.assertTrue(self.command.validate('tw'))
        self.assertTrue(self.command.validate('tW'))
        self.assertTrue(self.command.validate('t!'))

        # unacceptable commands
        self.assertFalse(self.command.validate('tAa'))
        self.assertFalse(self.command.validate('0a'))
        self.assertFalse(self.command.validate('a$'))
        self.assertFalse(self.command.validate('E'))
        self.assertFalse(self.command.validate('0e'))
        self.assertFalse(self.command.validate('z'))
        self.assertFalse(self.command.validate('T'))


class SelectionTestCase(MimCommandTestCase):

    def setUp(self):
        nav_command = NavigationCommand()
        self.command = SelectionCommand(nav_command)

    def test_selection(self):

        # 0123456789012345678901234
        # Hello World? Hello World!
        input_text = 'Hello World? Hello World!'

        text_status = TextStatus(input_text, SelectionCommand.COMMAND_SELECTION, 0, 0)
        command_vs = SelectionCommand.COMMAND_SELECTION + NavigationCommand.COMMAND_MOVE_TO_END
        command_v0 = SelectionCommand.COMMAND_SELECTION + NavigationCommand.COMMAND_MOVE_TO_BEGINNING
        command_vt = SelectionCommand.COMMAND_SELECTION + NavigationCommand.COMMAND_MOVE_TO_NEXT_MATCHED
        command_ve = SelectionCommand.COMMAND_SELECTION + NavigationCommand.COMMAND_MOVE_TO_WORD_END

        # TEST 'Hello World? Hello World!'
        # EXPECTED: '[Hello World?  Hello World!]'
        # COMMAND: v$
        text_status.current_command = command_vs
        text_status.start_position = 0
        text_status.end_position = 0
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=len(input_text))

        # TEST '[Hello World? Hello World!]'
        # EXPECTED: '[H]ello World? Hello World!'
        # COMMAND: v0
        text_status.current_command = command_v0
        text_status.start_position = 0
        text_status.end_position = len(input_text)
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=1)

        # TEST 'Hello World? Hello World[!]'
        # EXPECTED: '[Hello World? Hello World!]'
        # COMMAND: v0
        text_status.current_command = command_v0
        text_status.start_position = len(input_text) - 1
        text_status.end_position = len(input_text)
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=len(input_text))

        # TEST '[Hello] World? Hello World!'
        # EXPECTED: '[Hello World? Hello World!]'
        # COMMAND: v$
        text_status.current_command = command_vs
        text_status.start_position = 0
        text_status.end_position = 4
        self._assertions(text_status, start_pos_expected=0, end_pos_expected=len(input_text))

        # TEST 'Hello[ World?] Hello World!'
        # EXPECTED: 'Hello[ World? Hello ]World!'
        # COMMAND: vtw
        text_status.current_command = command_vt + 'w'
        text_status.start_position = 5
        text_status.end_position = 12
        self._assertions(text_status, start_pos_expected=5, end_pos_expected=19)

        # TEST 'H[ello ]World? Hello World!'
        # EXPECTED: 'H[ello ]World? Hello World!'
        # COMMAND: vtw
        text_status.current_command = command_vt + 'w'
        text_status.start_position = 1
        text_status.end_position = 6
        self._assertions(text_status, start_pos_expected=1, end_pos_expected=6)

        # TEST 'H[ello W]orld? Hello World!'
        # EXPECTED: 'H[ello World? Hello ]World!'
        # COMMAND: vtw
        text_status.current_command = command_vt + 'w'
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=1, end_pos_expected=19)

        # TEST 'H[ello W]orld? Hello World!'
        # EXPECTED: 'H[ello World?] Hello World!'
        # COMMAND: ve
        text_status.current_command = command_ve
        text_status.start_position = 1
        text_status.end_position = 7
        self._assertions(text_status, start_pos_expected=1, end_pos_expected=12)

    def test_validation(self):

        # acceptable commands
        self.assertTrue(self.command.validate('v0'))
        self.assertTrue(self.command.validate('v$'))
        self.assertTrue(self.command.validate('ve'))
        self.assertTrue(self.command.validate('vtw'))
        self.assertTrue(self.command.validate('vtW'))
        self.assertTrue(self.command.validate('vt!'))

        # unacceptable commands
        self.assertFalse(self.command.validate('0'))
        self.assertFalse(self.command.validate('$'))
        self.assertFalse(self.command.validate('e'))
        self.assertFalse(self.command.validate('tw'))
        self.assertFalse(self.command.validate('tW'))
        self.assertFalse(self.command.validate('t!'))
        self.assertFalse(self.command.validate('tAa'))
        self.assertFalse(self.command.validate('0a'))
        self.assertFalse(self.command.validate('a$'))
        self.assertFalse(self.command.validate('E'))
        self.assertFalse(self.command.validate('0e'))
        self.assertFalse(self.command.validate('z'))
        self.assertFalse(self.command.validate('T'))


if __name__ == '__main__':
    unittest.main()
