from typing import List

from commands import NavigationCommand, AppCommand, SelectionCommand
from mim import MimApp
from ui import SimpleMimUI, MimUI
from util import TextStatus


def main():

    mim_app = config_app()

    # collect the input text
    mim_app.input_text()

    # input and execute commands
    while True:
        if mim_app.get_command(mim_app.input_command()):
            mim_app.execute()
            mim_app.output_current_text_status()
        else:
            mim_app.output_text(MimUI.ERROR_COMMAND_NOT_RECOGNIZABLE)


def config_app() -> MimApp:
    # stack to keep the text status history
    command_history: List[TextStatus] = []

    # register commands
    nav_command = NavigationCommand()
    sel_command = SelectionCommand(nav_command)
    app_command = AppCommand(command_history)
    commands = [nav_command, sel_command, app_command]

    # config UI
    ui = SimpleMimUI()
    return MimApp(commands, ui, command_history)


if __name__ == "__main__":
    main()
