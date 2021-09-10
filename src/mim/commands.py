import sys
from typing import List

from util import TextStatus
import re


class Command:
    """
    The base Command interface defines operations that can be altered by
    decorators.
    """
    _re = None

    def execute(self, text_status: TextStatus) -> TextStatus:
        pass

    def validate(self, command_text: str) -> bool:
        if self._re.search(command_text):
            return True
        return False


class AppCommand(Command):

    # editor exit command
    COMMAND_EXIT = 'bye'
    COMMAND_REVERT = 'z'

    _re = re.compile(r'(^bye$)|(^z$)')

    def __init__(self, command_history: List[TextStatus]):
        self._command_history = command_history
        super().__init__()

    def execute(self, text_status: TextStatus) -> TextStatus:
        cur_command = text_status.current_command

        if cur_command == AppCommand.COMMAND_EXIT:
            AppCommand._sys_exit()
        elif cur_command == AppCommand.COMMAND_REVERT:
            return self._revert()

    @staticmethod
    def _sys_exit():
        print('Thank you for your time.  Alan Yan  alanyan@outlook.com ')
        sys.exit(0)

    def _revert(self) -> TextStatus:
        if len(self._command_history) > 1:
            self._command_history.pop()
        else:
            print('This is the very begninng. Calm down and enjoy it.')
        # need to pop "current" text status,  as it
        # will be re-pushed to history stack
        # after command executed in Mim App.
        return self._command_history.pop()


class NavigationCommand(Command):
    """
    Concrete Components provide default implementations of the operations.
    """
    _re = re.compile(r'(^[0$e]$)|(^t.$)')

    # command_list = ['0', '$', 'e', 't']
    COMMAND_MOVE_TO_BEGINNING = '0'
    COMMAND_MOVE_TO_END = '$'
    COMMAND_MOVE_TO_WORD_END = 'e'
    COMMAND_MOVE_TO_NEXT_MATCHED = 't'

    EMPTY_STRING = ' '

    def execute(self, text_status: TextStatus) -> TextStatus:

        cur_text = text_status.current_text
        cur_command = text_status.current_command

        if cur_command == NavigationCommand.COMMAND_MOVE_TO_BEGINNING:
            return NavigationCommand._move_to_beginning(cur_text)
        elif cur_command == NavigationCommand.COMMAND_MOVE_TO_END:
            return NavigationCommand._move_to_end(cur_text)
        elif cur_command == NavigationCommand.COMMAND_MOVE_TO_WORD_END:
            return NavigationCommand._move_to_word_end(cur_text, text_status.end_position)
        else:
            return NavigationCommand._move_to_next_matched(current_text=cur_text,
                                                           current_command=cur_command,
                                                           search_start_pos=text_status.start_position)

    @staticmethod
    def _move_to_beginning(current_text: str) -> TextStatus:
        return TextStatus(current_text=current_text,
                          current_command=NavigationCommand.COMMAND_MOVE_TO_BEGINNING,
                          start_pos=0,
                          end_pos=1)

    @staticmethod
    def _move_to_end(current_text: str) -> TextStatus:
        start_pos = len(current_text) - 1
        end_pos = len(current_text)
        return TextStatus(current_text=current_text,
                          current_command=NavigationCommand.COMMAND_MOVE_TO_END,
                          start_pos=start_pos,
                          end_pos=end_pos)

    @staticmethod
    def _move_to_word_end(current_text: str, current_position: int) -> TextStatus:

        # skip leading empty characters if any
        search_start_pos = current_position
        while (search_start_pos < len(current_text)) and (current_text[search_start_pos] == NavigationCommand.EMPTY_STRING):
            search_start_pos += 1

        if len(current_text) == search_start_pos:
            end_pos = current_position
        else:
            # find the end of word
            try:
                end_pos = current_text.index(NavigationCommand.EMPTY_STRING, search_start_pos)
            except ValueError:
                end_pos = len(current_text)

        return TextStatus(current_text=current_text,
                          current_command=NavigationCommand.COMMAND_MOVE_TO_WORD_END,
                          start_pos=end_pos-1,
                          end_pos=end_pos)

    @staticmethod
    def _move_to_next_matched(current_text: str, current_command: str, search_start_pos: int):

        search_char = current_command[1]
        try:
            end_pos = current_text.lower().index(search_char.lower(), search_start_pos)
        except ValueError:
            end_pos = search_start_pos + 1

        return TextStatus(current_text=current_text,
                          current_command=current_command,
                          start_pos=end_pos-1,
                          end_pos=end_pos)


class Decorator(Command):
    """
    The base Decorator class follows the same interface as the other components.
    The primary purpose of this class is to define the wrapping interface for
    all concrete decorators. The default implementation of the wrapping code
    might include a field for storing a wrapped component and the means to
    initialize it.
    """

    def __init__(self, command: Command) -> None:
        self._sub_command = command

    @property
    def sub_command(self) -> Command:
        """
        The Decorator delegates all work to the wrapped component.
        """

        return self._sub_command

    def execute(self, text_status: TextStatus) -> TextStatus:
        return self._sub_command.execute(text_status)


class SelectionCommand(Decorator):
    """
    Concrete Decorators call the wrapped object and alter its result in some
    way.
    """
    COMMAND_SELECTION = 'v'
    _re = re.compile(r'^v')

    def execute(self, text_status: TextStatus) -> TextStatus:
        """
        Decorators may call parent implementation of the operation, instead of
        calling the wrapped object directly. This approach simplifies extension
        of decorator classes.
        """
        command_text_sub = text_status.current_command[1:]
        start_pos_sub = text_status.end_position
        end_pos_sub = text_status.end_position+1
        text_status_sub = TextStatus(text_status.current_text,
                                     command_text_sub,
                                     start_pos_sub,
                                     end_pos_sub
                                     )
        # run navigation command
        text_status_new = self.sub_command.execute(text_status_sub)

        # update the new text status
        if text_status_new.end_position < text_status.start_position:
            text_status_new.end_position = text_status.end_position
        else:
            text_status_new.start_position = text_status.start_position
        text_status_new.current_command = text_status.current_command

        return text_status_new

    def validate(self, command_text: str) -> bool:
        if super().validate(command_text):
            return self.sub_command.validate(command_text[1:])
        return False
