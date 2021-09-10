from typing import List

from commands import Command
from ui import MimUI
from util import TextStatus


class MimApp:

    def __init__(self, available_commands: List[Command], ui: MimUI, command_history: List[TextStatus]) -> None:
        self._available_commands: List[Command] = available_commands
        self._ui: MimUI = ui
        self._cur_text_status: TextStatus = TextStatus(current_text="", current_command="")
        self._cur_command: Command

        self._command_history: List[TextStatus] = command_history

    def input_text(self):
        """
        Collect input text from UI
        """
        # gather text from user input
        input_text = self._ui.get_input_text()

        # save status
        self._cur_text_status.current_text = input_text
        self._cur_text_status.start_position = 0
        self._cur_text_status.end_position = 0
        self._cur_text_status.current_command = None
        self._command_history.append(self._cur_text_status)

    def input_command(self):
        """
        gather command text from UI
        """
        return self._ui.get_input_command()

    def get_command(self, command_text) -> Command:
        """
        find command by command text
        return None if no command found, command text is illegal
        """
        command = self._find_command(command_text)
        if command:
            self._cur_command = command
            self._cur_text_status.current_command = command_text
            return command
        else:
            return None   # validation failed, command doest not exist

    def output_current_text_status(self):
        """
        print current text status to UI
        """
        self._ui.output_text(self._cur_text_status.current_text,
                             self._cur_text_status.start_position,
                             self._cur_text_status.end_position
                             )

    def output_text(self, vaulue: str):
        """
        print information to UI
        """
        self._ui.output_text(vaulue)

    def execute(self):
        """
        run command and save text status to history, and
        refresh APP status
        """
        text_status_new = self._cur_command.execute(self._cur_text_status)

        # save status
        self._command_history.append(text_status_new)
        self._cur_text_status = text_status_new

    def _find_command(self, command_text: str) -> Command:
        for c in self._available_commands:
            if c.validate(command_text):
                return c
        return None
