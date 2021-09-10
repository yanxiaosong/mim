from abc import abstractmethod

from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError


class MimUI:

    ERROR_COMMAND_NOT_RECOGNIZABLE = 'Command is not recoganizable. Please try again'

    @abstractmethod
    def get_input_text(self) -> str:
        pass

    @abstractmethod
    def get_input_command(self) -> str:
        pass

    @abstractmethod
    def output_text(self, output_text, start_pos: int = 0, end_pos: int = 0):
        pass


class SimpleMimUI(MimUI):

    """
    A simple implementatin of MimUI
    """

    class InputTextValidator(Validator):
        INPUT_MAX_LENGTH: int = 30
        INPUT_MIN_LENGTH: int = 1

        def validate(self, document):
            try:
                if len(document.text) > self.INPUT_MAX_LENGTH or len(document.text) < self.INPUT_MIN_LENGTH:
                    raise ValueError()
            except ValueError:
                raise ValidationError(message="Input should not be empty and cannot exceed 30 characters",
                                      cursor_position=len(document.text))

    input_question = [
        {
            'type': "input",
            "name": "input_text",
            "message": "Input Text: ",
            "validate": InputTextValidator,
        },
    ]

    command_question = [
        {
            'type': "input",
            "name": "input_command",
            "message": "Command:    ",
        },
    ]

    def get_input_text(self):
        # collect the input text
        answers = prompt(self.input_question, style=custom_style_2)
        return answers.get("input_text")

    def get_input_command(self):
        # collect the input command
        answers = prompt(self.command_question, style=custom_style_2)
        return answers.get("input_command")

    def output_text(self, output_text, start_pos: int = 0, end_pos: int = 0) -> str:
        """
        Print out formatted content from start_pos(inclusive) to end_pos(exclusive)
        """
        if start_pos == end_pos:
            print(f'Output:         %s' % output_text)
            return output_text

        # format output
        formatted_text = output_text[0:start_pos] + "[" + output_text[start_pos:end_pos] + "]" + output_text[end_pos:]
        print(f'Output:         %s' % formatted_text)
        return formatted_text
