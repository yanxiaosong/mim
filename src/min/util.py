
class TextStatus:

    def __init__(self, current_text: str, current_command: str, start_pos: int = -1, end_pos: int = -1) -> None:
        self._current_text = current_text
        self._current_command = current_command
        self._start_pos = start_pos
        self._end_pos = end_pos

    @property
    def current_text(self) -> str:
        return self._current_text

    @current_text.setter
    def current_text(self, current_ext):
        self._current_text = current_ext

    @property
    def current_command(self) -> str:
        return self._current_command

    @current_command.setter
    def current_command(self, current_command: str):
        self._current_command = current_command

    @property
    def start_position(self):
        return self._start_pos

    @start_position.setter
    def start_position(self, start_position: int):
        self._start_pos = start_position

    @property
    def end_position(self):
        return self._end_pos

    @end_position.setter
    def end_position(self, end_position: int):
        self._end_pos = end_position
