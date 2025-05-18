##############################################################################
#                            FILE DESCRIPTION                                #
##############################################################################
# boggle.py WRITER : Adi Zuarets - 208708925, Renana Gabbai - 207743089
# intro cs ex11 2022-2023 DESCRIPTION: A program that creates a BOGGLE game
# and runs it

##############################################################################
#                                  IMPORT                                    #
##############################################################################
import tkinter as tk
from boggle_board_randomizer import *
from typing import *
from datetime import datetime, timedelta
from ex11_utils import *
import pygame

##############################################################################
#                                  PERMANENT                                #
##############################################################################

# Parameters
SIZE_BOARD = 4

# Font and color
FONT = "Gisha"
YELLOW_FRAME = '#DFC35F'
PURPLE_FRAME = "#7851A9"
PILL_BOX_COLOR = "#D6C37D"
MENU_FRAME_BOTTOM = "#553182"

# Reserved design templates
ACTIVE_BOTTOM_COLOR = {"activebackground": PURPLE_FRAME}
OUTER_FRAME = {"bg": YELLOW_FRAME, "highlightbackground": YELLOW_FRAME,
               "highlightthickness": 20}
MENU_BUTTON_STYLE = {"font": (FONT, 17), "foreground": "white",
                     "bg": PURPLE_FRAME, "highlightthickness": 2,
                     "highlightbackground": MENU_FRAME_BOTTOM}
MENU_FILL_BOX_STYLE = {"font": (FONT, 17), "bg": PILL_BOX_COLOR,
                       "highlightthickness": 2,
                       "highlightbackground": PURPLE_FRAME}
BORD_BUTTON_STYLE = {"font": (FONT, 38),
                     "borderwidth": 1, "relief": tk.RAISED,
                     "bg": PURPLE_FRAME, **ACTIVE_BOTTOM_COLOR}
DISPLAY_LABEL = {"bg": YELLOW_FRAME, "highlightbackground": YELLOW_FRAME,
                 "highlightthickness": 10}
POP_WINDOW_STYLE = {'font': (FONT, 12)}

# Extras paths
MUSIC_FILE = "Friends1.mp3"
IMG_PATH_TITLE = "label1.png"
# IMG_END_GAME = "joey.png"

# Reserved text
TITLE_MAIN_WINDOW = "Boggle- FRIENDS addition (6-99)"
SUBMIT_TEXT = "SUBMIT"
TIME_TEXT = "Time left:"
START_TIME = "03:00"
END_TIME = "00:00"
CUR_WORD_TEXT = "current word:"
SCORE_LABEL_TEXT = "Score:"
WORD_LABEL = "words list:"
START_TEXT = "START"
EMPTY = ""
EXIT_TEXT = "EXIT"
BLANK_BUTTON_TEXT = "?"
FILE_ALL_WORDS = 'boggle_dict.txt'
TITLE_GAME_OVER = "Do you want to play again?"
SCORE_MESSAGE = "good job!! \n you finish the game, your score is:"
QUESTION_REPLAY = "Do you want to play again?"
YES_TEXT = "YES"
NO_TEXT = " NO"

##############################################################################
#                                  FUNCTIONS                                #
##############################################################################


class BoggleGame:
    """This class create the amazing boggle game - friends addition"""
    _buttons: Dict[str, tk.Button] = {}

    def __init__(self):
        """A constructor for the boggle game. this constructor create the
         board game and all the objects that are shown in the game"""

        # Create variables
        self.__list_button = []
        self.__path = []
        self.__set_player_words = set()
        self.__set_of_words = set()
        self.__board = []
        self.__exit_button = None
        self.__submit_button = None
        self.__frame_button = None
        self.__start_button = None
        self.__words_list_menu = None
        self.__cur_player_words = None
        self.__score_menu = None
        self.__score = None
        self.__current_word_menu = None
        self.__cur_word = None
        self.timer_running = None
        self.__time_left_menu = None
        self.__cur_time_left = None
        self.__display_label = None
        self.__frame_player_words = None
        self.__lower_frame = None
        self.__menu_frame = None
        self.__outer_frame = None

        # main window
        root = tk.Tk()
        root.title(TITLE_MAIN_WINDOW)
        root.resizable(False, False)
        self.__main_window = root

        # initialize variables
        self.__board = randomize_board()
        self.__set_of_words = self.create_list_words()
        self.set_frame()
        self.set_labels()
        self.set_letter_button()
        self.set_submit_button()
        self.set_exit_button()
        self.set_start_button()

        # Extras
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)

    def set_frame(self) -> None:
        """This function creates the frames displayed in the game according
        to tkinter Gui software"""

        # Creates outer frame and the display
        self.__outer_frame = tk.Frame(self.__main_window, OUTER_FRAME)
        self.__outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__display_label = tk.Label(self.__outer_frame, DISPLAY_LABEL)
        self.__display_label.pack(side=tk.TOP, fill=tk.BOTH)

        # Creates menu frame
        self.__menu_frame = tk.Frame(self.__outer_frame, bg=PURPLE_FRAME)
        self.__menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Creates lower frame
        self.__lower_frame = tk.Frame(self.__outer_frame)
        self.__lower_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Creates player words frame
        self.__frame_player_words = tk.Frame(self.__outer_frame,
                                             bg=YELLOW_FRAME)
        self.__frame_player_words.pack(side=tk.RIGHT, fill=tk.BOTH,
                                       expand=True)

    def set_labels(self) -> None:
        """This function create the objects of the game
        according to the tinker and places them in the frames"""

        # Creates a costume label (main title)
        img = tk.PhotoImage(file=IMG_PATH_TITLE)
        label_img = tk.Label(self.__display_label, image=img)
        label_img.image = img
        label_img.pack(side=tk.TOP)

        # Creates timer label
        tk.Label(self.__menu_frame, width=11, text=TIME_TEXT, height=2,
                 **MENU_BUTTON_STYLE).grid(row=2, column=0)
        self.__cur_time_left = START_TIME
        self.__time_left_menu = tk.Label(self.__menu_frame, width=11,
                                         text=str(self.__cur_time_left),
                                         height=2, **MENU_FILL_BOX_STYLE)
        self.__time_left_menu.grid(row=2, column=1)
        self.timer_running = False

        # Creates cur word label
        tk.Label(self.__menu_frame, width=23,
                 text=CUR_WORD_TEXT, height=2, **MENU_BUTTON_STYLE).grid(
            row=3, column=0, columnspan=3)
        self.__cur_word = EMPTY
        self.__current_word_menu = tk.Label(self.__menu_frame, width=23,
                                            text=self.__cur_word, height=2,
                                            **MENU_FILL_BOX_STYLE)
        self.__current_word_menu.grid(row=4, column=0, columnspan=3)

        # Creates score grade label
        tk.Label(self.__menu_frame, width=11,
                 text=SCORE_LABEL_TEXT, height=2,
                 **MENU_BUTTON_STYLE).grid(row=6, column=0)
        self.__score = 0
        self.__score_menu = tk.Label(self.__menu_frame, width=11,
                                     text=self.__score, height=2,
                                     **MENU_FILL_BOX_STYLE)
        self.__score_menu.grid(row=6, column=1)

        # Creates words_menu_label
        tk.Label(self.__frame_player_words, width=21, text=WORD_LABEL,
                 height=1, **MENU_BUTTON_STYLE).grid(row=0, column=0,
                                                       columnspan=3)
        self.__cur_player_words = EMPTY
        self.__words_list_menu = tk.Label(self.__frame_player_words, width=21,
                                          text=self.__cur_player_words,
                                          height=13, **MENU_FILL_BOX_STYLE)
        self.__words_list_menu.grid(row=1, column=0, columnspan=3)

    def set_start_button(self) -> None:
        """This function initializes and places the start button"""
        self.__start_button = tk.Button(self.__menu_frame, width=23,
                                        text=START_TEXT, height=1,
                                        command=self.start_pressed,
                                        **MENU_BUTTON_STYLE,
                                        **ACTIVE_BOTTOM_COLOR)
        self.__start_button.grid(row=0, column=0, columnspan=3)

    def start_pressed(self) -> None:
        """This function is responsible for the operation of the start button.
        Makes the game start running when the button is pressed"""

        # start timer
        self.__cur_time_left = datetime.now() + timedelta(minutes=3)
        self.update_timer()

        # set the state of start, submit, exit buttons
        self.__start_button.config(state="disabled")
        self.__submit_button.config(state="active")
        self.__exit_button.config(state="active")

        # set the letter buttons
        for row in range(SIZE_BOARD):
            for col in range(SIZE_BOARD):
                self.__list_button.append(
                    self.make_button(self.__board[row][col], row, col, True))

    def set_letter_button(self) -> None:
        """This function initializes and places the letters button"""
        self.__frame_button = tk.Frame(self.__outer_frame)
        self.create_buttons_in_lower_frame()

    def update_timer(self) -> None:
        """This function is responsible for the timer
         operation and stopping the game when the game is over"""

        # Set timer fot game
        time_remaining = self.__cur_time_left - datetime.now()
        self.__time_left_menu.config(text=str(time_remaining)[2:7])
        self.__main_window.after(1000, self.update_timer)

        # Stop conditions
        if str(time_remaining)[2:7] == END_TIME:
            self.game_over()

    def make_button(self, text_board: str, cur_row: int,
                    cur_col: int, active: bool = False, ) -> tk.Button:
        """This function creates the game letter button"""

        # set letter button
        button = tk.Button(self.__lower_frame, text=text_board,
                           **BORD_BUTTON_STYLE, state="disabled",
                           command=lambda i=cur_row, j=cur_col:
                           self.letter_button_pressed(i, j))

        if active:
            button.config(state="active")

        button.grid(row=cur_row, column=cur_col, sticky=tk.NSEW)
        self._buttons[text_board] = button

        return button

    def create_buttons_in_lower_frame(self) -> None:
        """This function places the game letter button"""

        # Creates grid buttons
        for i in range(SIZE_BOARD):
            tk.Grid.columnconfigure(self.__frame_button, i, weight=1)
        for i in range(SIZE_BOARD):
            tk.Grid.rowconfigure(self.__frame_button, i, weight=1)

        # Creates button list
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                self.__list_button.append(
                    self.make_button(BLANK_BUTTON_TEXT, row, col))

    def letter_button_pressed(self, row: int, col: int) -> None:
        """This function create the player's current
         word according to the player's press on the game letters"""
        self.__path.append((row, col))
        self.__cur_word = path_to_word(self.__board, self.__path)
        self.__current_word_menu.config(text=self.__cur_word)

    def set_submit_button(self) -> None:
        """This function initializes and places the sumit button"""
        self.__submit_button = tk.Button(self.__menu_frame, width=23,
                                         state="disabled",
                                         command=self.submit_pressed,
                                         text=SUBMIT_TEXT, height=1,
                                         **MENU_BUTTON_STYLE,
                                         **ACTIVE_BOTTOM_COLOR)
        self.__submit_button.grid(row=5, column=0, columnspan=3)

    def submit_pressed(self) -> None:
        """This function works when the player presses the submit button.
         The function checks if the word is in the words' dictionary,
         if so - raises the score for the player and adds
        the word to the list of words chosen by the player"""

        word_player = is_valid_path(self.__board, self.__path,
                                    self.__set_of_words)

        # Checks if path and word valid
        if word_player is not None and word_player not in \
                self.__set_player_words:

            self.__score += (len(self.__path) ** 2)
            self.__score_menu.config(text=str(self.__score))
            self.__set_player_words.add(word_player)
            player_word_print = lambda x: '\n'.join(x)
            self.__words_list_menu.config(
                text=player_word_print(self.__set_player_words))

        # Set display
        self.__cur_word = EMPTY
        self.__current_word_menu.config(text=self.__cur_word)
        self.__path = []

    def create_list_words(self) -> set:
        """This function opens the Boggle dict file and call to another
        function which returns all the possible paths to create words on the
        current game board"""
        with open(FILE_ALL_WORDS, 'r') as f:
            list_index_names = f.read().splitlines()
        return filter_words(self.__board, list_index_names)[1]

    def set_exit_button(self) -> None:
        """This function initializes and places the exit button"""
        self.__exit_button = tk.Button(self.__menu_frame, width=23,
                                       state="disabled",
                                       command=self.game_over,
                                       text=EXIT_TEXT, height=1,
                                       **MENU_BUTTON_STYLE,
                                       **ACTIVE_BOTTOM_COLOR)
        self.__exit_button.grid(row=1, column=0, columnspan=3)

    def set_end_game_message(self) -> None:
        """ This function create a pop window when the game is over/
         the player chooses to end the game. The player is asked if he wants
         to play again, if so the game is restarted, else the game is ended"""

        # Creates end game message window
        result = tk.Tk()
        result.geometry(
            "300x200+{}+{}".format(result.winfo_screenwidth() // 2 - 150,
                                   result.winfo_screenheight() // 2 - 100))
        result.title(TITLE_GAME_OVER)
        result.grab_set()

        # Creates a label message of score
        label_message_score = tk.Label(result,
                                       text=SCORE_MESSAGE, **POP_WINDOW_STYLE)
        label_message_score.pack()
        label_score = tk.Label(result, text=self.__score, **POP_WINDOW_STYLE,
                               bg=PURPLE_FRAME)
        label_score.pack()

        # Creates a label message of question yes or no
        label_question = tk.Label(result, text=QUESTION_REPLAY,
                                  **POP_WINDOW_STYLE)
        label_question.pack()

        # Creates button to label
        yes_button = tk.Button(result, text=YES_TEXT, **POP_WINDOW_STYLE,
                               bg=YELLOW_FRAME, command=lambda:
                               (result.destroy(), self.restart_game()))
        yes_button.pack(anchor="center")
        no_button = tk.Button(result, text=NO_TEXT, **POP_WINDOW_STYLE,
                              bg=YELLOW_FRAME, command=lambda:
                              (result.destroy(), self.__main_window.destroy()))
        no_button.pack(anchor="center")

        # friends_img = tk.PhotoImage(file="joey.png")
        # friends_label_img = tk.Label(result, image=friends_img)
        # friends_label_img.image = friends_img
        # friends_label_img.pack(anchor="center")

    def run(self) -> None:
        """This function activates the game -
         opens the game window and activates the opening song"""
        pygame.mixer.music.play()
        return self.__main_window.mainloop()

    def game_over(self) -> None:
        """This function ends the game and pops the end of game message"""
        self.__cur_time_left = END_TIME
        self.__time_left_menu.config(text=self.__cur_time_left)
        self.set_end_game_message()

    def restart_game(self) -> None:
        """This function restart the game -
        redefines the relevant variables for a new game"""

        # initialize buttons
        self.__board = randomize_board()
        self.__start_button.config(state="active")
        for row in range(SIZE_BOARD):
            for col in range(SIZE_BOARD):
                self.__list_button.append(self.make_button(BLANK_BUTTON_TEXT,
                                                           row, col))

        # initialize display
        self.__set_of_words = self.create_list_words()
        self.__words_list_menu.config(text=EMPTY)
        self.__set_player_words = set()
        self.__path = []
        self.__score = 0
        self.__score_menu.config(text=str(self.__score))
        self.__cur_word = EMPTY
        self.__current_word_menu.config(text=self.__cur_word)

        self.run()


if __name__ == '__main__':
    game = BoggleGame()
    game.run()
