"""This file implement console version of program"""
import sys
from colorama import Fore, Back, Style, init
import logging

LOGGER = logging.getLogger("console_lines")
logging.basicConfig(filename="console_lines.log", level=logging.INFO)

try:
    from core import *
    from driver import *
except Exception as e:
    LOGGER.error(e)
    sys.exit(f"Game modules not found: {e}")

COLOR = {1: Fore.RED, 2: Fore.GREEN, 3: Fore.YELLOW, 4: Fore.BLUE, 5: Fore.MAGENTA, 6: Fore.CYAN, 7: Fore.WHITE}
ALL_ACTIONS = ["help", "make_step", "reset", "end"]


def print_field(game_field):
    """Print game_field in console"""
    counter = 0
    print("\n     0 1 2 3 4 5 6 7 8")
    print("    ------------------")
    for rows in range(game_field.game.height):
        string = f" {counter} | "
        for columns in range(game_field.game.width):
            if game_field.game.field[rows][columns] is None:
                string += Fore.BLACK + Style.BRIGHT + "X " + Style.RESET_ALL
            else:
                ball_color = game_field.game.get_color_of_ball(columns, rows)
                string += COLOR.get(ball_color) + Style.BRIGHT + "O " + Style.RESET_ALL
        if counter == 1:
            string += Style.BRIGHT + f"         Scores: {game_field.game.score}" + Style.RESET_ALL
        counter += 1
        print(string)


class ConsoleMode:
    """Class console version"""

    def __init__(self):
        """Initialize class"""
        init()
        self._init_field()
        self.arguments = None

    def _init_field(self):
        """Initialize field for play"""
        player_name = input("\nInput your name: ")
        if player_name == "" or player_name is None:
            player_name = "Player"
        self.game = Field(player=player_name)
        self.game.set_next_balls()
        LOGGER.info(f"Game field was initialized. Size: 9. Player name: {player_name}")
        self.print_help()
        print_field(self)

    def print_help(self):
        """Print help"""
        print("\n=================================================\n"
              "This is console version of game \"Lines\"\n "
              " Possible commands:\n"
              "  # make_step [start x] [start y] [end x] [end y]\n"
              "  # reset\n"
              "  # end\n"
              "=================================================")

    def reset_game(self):
        """Reset the game"""
        self.game.refresh_field()
        print_field(self)
        LOGGER.info("Game was restart.")

    def finish_game(self):
        """Finish the game"""
        print("{}, you scored : {} points".format(self.game.player, self.game.score))
        add_record(self.game.player, self.game.score)
        LOGGER.info(f"Game over with {self.game.score} points")
        sys.exit("Game Over!")

    def make_step(self):
        """Make step"""
        array = []
        if self.arguments is None or len(self.arguments) < 4:
            raise IncorrectCommand
        for argument in self.arguments:
            if int(argument) < 0 or int(argument) > 8:
                raise IncorrectStep
            array.append(int(argument))
        else:
            if self.game.try_move(array[0], array[1], array[2], array[3]):
                self.game.make_step(array[0], array[1], array[2], array[3])
                ball_for_delete = self.game.find_full_lines(array[2], array[3])
                if ball_for_delete is None:
                    try:
                        self.game.set_next_balls()
                        LOGGER.info(f"Following {self.game.number_of_next_ball} balls are installed.")
                    except FieldFullException:
                        self.finish_game()
                        LOGGER.info("Field full. Game over.")
                else:
                    self.game.delete_full_lines(ball_for_delete)
                    for coordinates in self.game.set_balls:
                        array = self.game.find_full_lines(coordinates[0], coordinates[1])
                        if array is not None:
                            self.game.delete_full_lines(array)
                            LOGGER.info(
                                f"Found full lines: {ball_for_delete} and deleted. Score: {self.game.score}.")
            else:
                raise IncorrectStep()
        self.arguments = None
        print_field(self)

    actions = {"help": print_help,
               "reset": reset_game,
               "end": finish_game,
               "make_step": make_step}


class IncorrectCommand(Exception):
    """Incorrect command error"""
    pass


class IncorrectStep(Exception):
    """Incorrect step"""
    pass


def read_argument(game_field):
    """Read argument"""
    while True:
        arguments = input("\n # ").strip()
        if arguments == "":
            continue
        else:
            array_arguments = arguments.split(" ")
            try:
                finish_arguments = get_finish_arguments(array_arguments)
                command_handler(finish_arguments, game_field)
            except IncorrectCommand:
                print("Incorrect command")
            except IncorrectStep:
                print("Incorrect step")


def command_handler(finish_arguments, game_field):
    """Command_handler"""
    first_argument = finish_arguments[0]
    if first_argument not in ALL_ACTIONS:
        raise IncorrectCommand
    else:
        finish_arguments.pop(0)
        game_field.arguments = finish_arguments
        game_field.actions.get(first_argument)(game_field)


def get_finish_arguments(array_arguments):
    """Get finish argument from input"""
    finish_arguments = []
    for argument in array_arguments:
        if argument == " " or argument == "":
            continue
        else:
            finish_arguments.append(argument)
        if len(finish_arguments) > 5:
            raise IncorrectCommand
    if len(finish_arguments) == 1 or len(finish_arguments) == 5:
        return finish_arguments
    else:
        raise IncorrectCommand


if __name__ == '__main__':
    game = ConsoleMode()
    read_argument(game)
