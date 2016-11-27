from tkinter import *
from tkinter import ttk
from player import PlayerType, HumanPlayer, create_player
from board import Board, BLACK, WHITE
import threading
from tkinter import messagebox

PLAYER_FOREGROUND = '#A5201C'
PLAYER_BACKGROUND = '#74A1E0'
DISABLED_COLOR = 'yellow3'


class Othello:
    def __init__(self, master: Tk):

        master.title('Othello (Reversi) Game')
        master.resizable(False, False)

        self.master = master  # type: Tk
        self.move_thread = threading.Thread()
        self.board = Board()  # type: Board
        self.last_move = tuple()  # type: tuple
        self.last_color = 0
        self.all_moves = []
        self.move_history_index = 0
        self.game_started = False
        self.stop_timer = False

        # ++++++++++++++++++++++++++++++ Frames ++++++++++++++++++++++++++++++++++

        # +++++++++++++++++++++++++++ Header Frame +++++++++++++++++++++++++++++++
        # Header frame
        self.header_frame = ttk.Frame(self.master, name='header_frame')
        self.header_frame.pack(fill=X)

        # Frame for configuring players
        self.player_config_label = ttk.Label(text='Player Configuration:',
                                             font=('Arial', 12, 'bold', 'italic', 'underline'),
                                             foreground=PLAYER_FOREGROUND, background=PLAYER_BACKGROUND,
                                             name='player_config_label')
        self.players_frame = ttk.LabelFrame(self.header_frame, labelwidget=self.player_config_label,
                                            name='players_frame')
        self.players_frame.pack(fill=X, padx=5, pady=(5, 0))

        # Frame containing buttons
        self.buttons_frame = ttk.Frame(self.header_frame, name='buttons_frame')
        self.buttons_frame.pack(fill=X, pady=5)
        # ------------------------------------------------------------------------

        # ++++++++++++++++++++++++++ Content Frame +++++++++++++++++++++++++++++++
        # Content frame containing game and table
        self.content_frame = ttk.Frame(self.master, name='content_frame')
        self.content_frame.pack()

        # Frames containing letters
        self.left_numbers = ttk.Frame(self.content_frame, name='left_numbers')
        self.right_numbers = ttk.Frame(self.content_frame, name='right_numbers')
        self.left_numbers.grid(row=1, column=0)
        self.right_numbers.grid(row=1, column=2)

        # Frames containing numbers
        self.top_letters = ttk.Frame(self.content_frame, name='top_letters')
        self.bottom_letters = ttk.Frame(self.content_frame, name='bottom_letters')
        self.top_letters.grid(row=0, column=1)
        self.bottom_letters.grid(row=2, column=1)

        # Frame containing the game
        self.game_frame = ttk.Frame(self.content_frame, name='game_frame')
        self.game_frame.grid(row=1, column=1)
        # ------------------------------------------------------------------------

        # +++++++++++++++++++++++++++ Footer Frame +++++++++++++++++++++++++++++++
        self.footer_frame = ttk.Frame(self.master, name='footer_frame')
        self.footer_frame.pack(fill=X)
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------

        # ++++++++++++++++++++++ Images and Icons ++++++++++++++++++++++++++++++++
        image_dir = 'Images/Smaller'

        # Images for cells
        self.black_token = PhotoImage(file='{}/black.gif'.format(image_dir))
        self.white_token = PhotoImage(file='{}/white.gif'.format(image_dir))
        self.empty_token = PhotoImage(file='{}/empty.gif'.format(image_dir))
        self.last_move_black = PhotoImage(file='{}/last_move_black.gif'.format(image_dir))
        self.last_move_white = PhotoImage(file='{}/last_move_white.gif'.format(image_dir))
        self.valid_move = PhotoImage(file='{}/valid_move.gif'.format(image_dir))

        # {} for the table
        self.letters = [None] * 8
        self.numbers = [None] * 8
        self.letters[0] = PhotoImage(file='{}/A.gif'.format(image_dir))
        self.letters[1] = PhotoImage(file='{}/B.gif'.format(image_dir))
        self.letters[2] = PhotoImage(file='{}/C.gif'.format(image_dir))
        self.letters[3] = PhotoImage(file='{}/D.gif'.format(image_dir))
        self.letters[4] = PhotoImage(file='{}/E.gif'.format(image_dir))
        self.letters[5] = PhotoImage(file='{}/F.gif'.format(image_dir))
        self.letters[6] = PhotoImage(file='{}/G.gif'.format(image_dir))
        self.letters[7] = PhotoImage(file='{}/H.gif'.format(image_dir))
        self.numbers[0] = PhotoImage(file='{}/1.gif'.format(image_dir))
        self.numbers[1] = PhotoImage(file='{}/2.gif'.format(image_dir))
        self.numbers[2] = PhotoImage(file='{}/3.gif'.format(image_dir))
        self.numbers[3] = PhotoImage(file='{}/4.gif'.format(image_dir))
        self.numbers[4] = PhotoImage(file='{}/5.gif'.format(image_dir))
        self.numbers[5] = PhotoImage(file='{}/6.gif'.format(image_dir))
        self.numbers[6] = PhotoImage(file='{}/7.gif'.format(image_dir))
        self.numbers[7] = PhotoImage(file='{}/8.gif'.format(image_dir))

        # Icons for buttons
        self.next_icon = PhotoImage(file='Images/next.gif')
        self.previous_icon = PhotoImage(file='Images/previous.gif')
        self.play_icon = PhotoImage(file='Images/play.gif')
        self.reset_icon = PhotoImage(file='Images/reset.gif')
        self.stop_icon = PhotoImage(file='Images/stop.gif')
        self.start_icon = PhotoImage(file='Images/start.gif')
        # ------------------------------------------------------------------------

        # Buttons for playing the game
        button_width = 13
        self.make_move_button = ttk.Button(self.buttons_frame, text='Make Move', command=self.make_move,
                                           name='make_move_button',
                                           width=button_width)
        self.make_move_button.img = self.play_icon
        self.make_move_button.config(image=self.make_move_button.img, compound=LEFT)
        #self.make_move_button.pack(side=LEFT, padx=10)

        self.previous_move_button = ttk.Button(self.buttons_frame, text='Previous Move',
                                               name='previous_move_button',
                                               command=self.previous_move, width=button_width)
        self.previous_move_button.img = self.previous_icon
        self.previous_move_button.config(image=self.previous_move_button.img, compound=LEFT)
        self.previous_move_button.pack(side=LEFT, padx=10)

        self.next_move_button = ttk.Button(self.buttons_frame, text='Next Move', command=self.next_move,
                                           name='next_move_button',
                                           width=button_width)
        self.next_move_button.img = self.next_icon
        self.next_move_button.config(image=self.next_move_button.img, compound=LEFT)
        self.next_move_button.pack(side=LEFT, padx=10)

        self.reset_button = ttk.Button(self.buttons_frame, text='Reset Game', command=self.reset_game,
                                       name='reset_button',
                                       width=button_width)
        self.reset_button.img = self.reset_icon
        self.reset_button.config(image=self.reset_button.img, compound=LEFT, state=DISABLED)
        self.reset_button.pack(side=RIGHT, padx=10)

        # +++++++++++++++++++++++++ Configure players ++++++++++++++++++++++++++++
        # Controls for configuring players
        self.black_player_name = StringVar()
        self.white_player_name = StringVar()
        self.black_player_type = StringVar()
        self.white_player_type = StringVar()
        self.black_player_level = IntVar()
        self.white_player_level = IntVar()
        self.time_out_value = IntVar()

        # Default player types and levels
        self.black_player_type.set(PlayerType.human.value)
        self.white_player_type.set(PlayerType.human.value)
        self.black_player_level.set(1)
        self.white_player_level.set(1)
        self.time_out_value.set(20)

        # +++++++++++++ Black player configuration frame and controls +++++++++++++
        # Container grid
        self.black_player_label = ttk.Label(
            text='Black',
            font=('Arial', 12, 'bold', 'underline'),
            foreground='black',
            background=PLAYER_BACKGROUND)
        self.black_player_frame = ttk.LabelFrame(
            self.players_frame,
            name='black_player_frame',
            labelwidget=self.black_player_label)
        self.black_player_frame.grid(row=0, column=0, sticky=W, rowspan=3)

        # Label and entry for the name
        ttk.Label(self.black_player_frame, text='Name: ',
                  background=PLAYER_BACKGROUND).grid(row=0, column=0, sticky='e')
        self.black_player_name_entry = ttk.Entry(
            self.black_player_frame,
            name='black_player_name_entry',
            textvariable=self.black_player_name)
        self.black_player_name_entry.grid(row=0, column=1, padx=5, sticky=N+S+E+W)

        # Label and combobox for the type
        ttk.Label(self.black_player_frame, text='Type: ',
                  background=PLAYER_BACKGROUND).grid(row=1, column=0, sticky='e')
        self.black_player_type_combo = ttk.Combobox(
            self.black_player_frame,
            values=list(member.value for _, member in PlayerType.__members__.items()),
            name='black_player_type_combo',
            textvariable=self.black_player_type)
        self.black_player_type_combo.bind(
            '<<ComboboxSelected>>', lambda event: self.update_level_spinbox(event, BLACK))
        self.black_player_type_combo.grid(row=1, column=1, padx=5, sticky='w')

        # Label and spin-box for the level
        ttk.Label(self.black_player_frame, text='Level: ',
                  background=PLAYER_BACKGROUND).grid(row=2, column=0, sticky=E)

        self.black_level_spin = Spinbox(
            self.black_player_frame,
            from_=1, to=6,
            width=18,
            name='black_player_level_spin',
            textvariable=self.black_player_level)
        self.black_level_spin.configure(state=DISABLED, disabledbackground=DISABLED_COLOR)
        self.black_level_spin.grid(row=2, column=1, sticky='nsew', padx=5)
        # -------------------------------------------------------------------------

        # +++++++++++++ White player configuration frame and controls +++++++++++++
        # Container grid
        self.white_player_label = ttk.Label(
            text='White',
            font=('Arial', 12, 'bold', 'underline'),
            foreground='white',
            background=PLAYER_BACKGROUND)
        self.white_player_frame = ttk.LabelFrame(
            self.players_frame,
            name='white_player_frame',
            labelwidget=self.white_player_label)
        self.white_player_frame.grid(row=0, column=1, sticky=W, rowspan=3)

        # Label and entry for the name
        ttk.Label(self.white_player_frame, text='Name: ',
                  background=PLAYER_BACKGROUND).grid(row=0, column=0, sticky='e')
        self.white_player_name_entry = ttk.Entry(
            self.white_player_frame,
            name='white_player_name_entry',
            textvariable=self.white_player_name)
        self.white_player_name_entry.grid(row=0, column=1, padx=5, sticky='nsew')

        # Label and combobox for the type
        ttk.Label(self.white_player_frame, text='Type: ',
                  background=PLAYER_BACKGROUND).grid(row=1, column=0, sticky='e')
        self.white_player_type_combo = ttk.Combobox(
            self.white_player_frame,
            values=list(member.value for _, member in PlayerType.__members__.items()),
            name='white_player_type_combo',
            textvariable=self.white_player_type)
        self.white_player_type_combo.bind(
            '<<ComboboxSelected>>', lambda event: self.update_level_spinbox(event, WHITE))
        self.white_player_type_combo.grid(row=1, column=1, padx=5, sticky='w')

        # Label and spin-box for the level
        ttk.Label(self.white_player_frame, text='Level: ',
                  background=PLAYER_BACKGROUND).grid(row=2, column=0, sticky='e')
        self.white_player_level_spin = Spinbox(
            self.white_player_frame,
            from_=1, to=6,
            width=18,
            name='white_player_level_spin',
            textvariable=self.white_player_level)
        self.white_player_level_spin.configure(state=DISABLED, disabledbackground=DISABLED_COLOR)
        self.white_player_level_spin.grid(row=2, column=1, sticky='nsew', padx=5)
        # -------------------------------------------------------------------------

        # Time out label and spin-box
        ttk.Label(self.players_frame, text='Move Time Out (seconds):',
                  background=PLAYER_BACKGROUND).grid(row=0, column=2, sticky=W)
        self.time_out_spin = Spinbox(
            self.players_frame,
            from_=1, to=60,
            name='time_out_spin',
            textvariable=self.time_out_value)
        self.time_out_spin.grid(row=1, column=2, sticky='ew')

        # Start game button
        self.start_game_button = ttk.Button(self.players_frame, text='Start Game',
                                            name='start_game_button',
                                            command=self.start_game)
        self.start_game_button.img = self.start_icon
        self.start_game_button.configure(image=self.start_game_button.img, compound=LEFT)
        self.start_game_button.grid(row=2, column=2, sticky='ew')

        # Configure column weights on the parent
        self.players_frame.grid_columnconfigure(0, weight=1)
        self.players_frame.grid_columnconfigure(1, weight=1)
        self.players_frame.grid_columnconfigure(2, weight=1)

        # Set up the players
        self.players = dict()
        self.current_player = 0
        # ------------------------------------------------------------------------

        # Add number labels to their frames
        for i in range(len(self.numbers) - 1, -1, -1):
            left_letter_label = ttk.Label(self.left_numbers)
            right_letter_label = ttk.Label(self.right_numbers)
            left_letter_label.img = self.numbers[i]
            right_letter_label.img = self.numbers[i]
            left_letter_label.config(image=left_letter_label.img)
            right_letter_label.config(image=right_letter_label.img)
            left_letter_label.pack(padx=5, pady=5)
            right_letter_label.pack(padx=5, pady=5)

        # Add letter labels to their frame
        for i in range(len(self.letters)):
            top_number_label = ttk.Label(self.top_letters)
            bottom_number_label = ttk.Label(self.bottom_letters)
            top_number_label.img = self.letters[i]
            bottom_number_label.img = self.letters[i]
            top_number_label.config(image=top_number_label.img)
            bottom_number_label.config(image=bottom_number_label.img)
            top_number_label.pack(side=LEFT, padx=5, pady=5)
            bottom_number_label.pack(side=LEFT, padx=5, pady=5)

        # Status display controls in the footer frame
        # +++++++++++++++++++++++++++++++ Information frame +++++++++++++++++++++++++++++++++
        self.info_frame = ttk.Frame(self.footer_frame, name='info_frame')  # Frame for turn and move labels
        self.info_frame.pack(fill=X, padx=15, pady=5)

        self.turn_label = ttk.Label(self.info_frame, name='turn_label')
        self.turn_label.config(background='green', foreground='yellow', text='Current player:',
                               width=10,
                               font=('Arial', 10))
        self.turn_label.grid(row=0, column=0, ipady=5, sticky='nsew')

        self.turn_color_label = ttk.Label(self.info_frame, name='turn_color_label')
        self.turn_color_label.config(background='green', foreground='white', text='NONE',
                                     width=20,
                                     font=('Arial', 10, 'bold', 'italic'))
        self.turn_color_label.grid(row=0, column=1, ipady=5, sticky='nsew')

        self.last_move_label = ttk.Label(self.info_frame,
                                         name='last_move_label',
                                         width=20,
                                         font=('Arial', 10))
        self.last_move_label.config(background='blue', foreground='yellow', anchor='e')
        self.last_move_label.grid(row=0, column=2, ipady=5, sticky='nsew')

        # Adjust column weights for info grid
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=2)
        self.info_frame.grid_columnconfigure(2, weight=1)
        # -----------------------------------------------------------------------------------

        # ++++++++++++++++++++++++++++++++++ Progress bar +++++++++++++++++++++++++++++++++++
        self.progress_bar = ttk.Progressbar(self.footer_frame, orient=HORIZONTAL, name='progress_bar')
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.pack(fill=X, padx=15)
        # -----------------------------------------------------------------------------------

        # +++++++++++++++++++++++++++++++ Move information frame ++++++++++++++++++++++++++++
        self.info2_frame = ttk.Frame(self.footer_frame, name='info2_frame')
        self.info2_frame.pack(fill=X, padx=15, pady=5)

        self.move_history_label = ttk.Label(self.info2_frame, name='move_history_label')
        self.move_history_label.config(
            background='indian red',
            foreground='white',
            width=43,
            text='Current player:',
            font=('Arial', 10))
        self.move_history_label.grid(row=0, column=0, ipady=5, sticky='nsew')

        self.timer_label = ttk.Label(self.info2_frame,
                                     name='timer_label',
                                     width=10,
                                     font=('Arial', 10))
        self.timer_label.config(background='bisque2', foreground='black')
        self.timer_label.grid(row=0, column=1, ipady=5, sticky='nsew')

        self.info2_frame.grid_columnconfigure(0, weight=1)
        self.info2_frame.grid_columnconfigure(1, weight=1)
        # -----------------------------------------------------------------------------------

        # +++++++++++++++++++++++++++ Board grid +++++++++++++++++++++++++++++++++
        # Initialize all the cells to empty
        self.labels = [None] * 8
        for i in range(8):
            self.labels[i] = [None] * 8

        # Create labels corresponding to cells and add them to the game frame
        for label_row in range(8):
            for label_column in range(8):
                self.labels[label_row][label_column] = ttk.Label(self.game_frame)
                new_label = self.labels[label_row][label_column]  # type: ttk.Label
                new_label.row = label_row
                new_label.column = label_column
                new_label.grid(row=7 - label_column, column=label_row, padx=5, pady=5)
        # ------------------------------------------------------------------------

        # ++++++++++++++++++++++++++++++ Styles ++++++++++++++++++++++++++++++++++
        self.style = ttk.Style()

        # Configure styles
        self.style.configure('GameFrame.TFrame', background='black')
        self.content_frame.config(style='GameFrame.TFrame')
        self.game_frame.config(style='GameFrame.TFrame')
        self.left_numbers.config(style='GameFrame.TFrame')
        self.right_numbers.config(style='GameFrame.TFrame')
        self.top_letters.config(style='GameFrame.TFrame')
        self.bottom_letters.config(style='GameFrame.TFrame')

        self.style.configure('FooterFrame.TFrame', background='gray')
        self.footer_frame.config(style='FooterFrame.TFrame')

        self.style.configure('HeaderFrame.TFrame', background=PLAYER_BACKGROUND)
        self.header_frame.configure(style='HeaderFrame.TFrame')
        self.buttons_frame.configure(style='HeaderFrame.TFrame')
        self.players_frame.configure(style='HeaderFrame.TFrame')
        self.black_player_frame.configure(style='HeaderFrame.TFrame')
        self.white_player_frame.configure(style='HeaderFrame.TFrame')

        self.update()
        # ------------------------------------------------------------------------

        # Put the window in the center of the screen
        master.update_idletasks()
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width, window_height = tuple(int(_) for _ in master.geometry().split('+')[0].split('x'))
        window_x = screen_width // 2 - window_width // 2
        window_y = screen_height // 2 - window_height // 2 - 35
        master.geometry('{}x{}+{}+{}'.format(window_width, window_height, window_x, window_y))

    def update(self):
        for label_row in range(8):
            for label_column in range(8):
                cell_color = self.board[label_row][label_column]
                cell_label = self.labels[label_row][label_column]  # type: ttk.Label

                move = (label_row, label_column)
                valid_moves = self.board.get_legal_moves()

                # Highlight last move made by white or black
                if cell_color == -1:
                    cell_label.img = self.black_token if move != self.last_move else self.last_move_black
                elif cell_color == 1:
                    cell_label.img = self.white_token if move != self.last_move else self.last_move_white
                # Highlight next valid moves
                else:
                    cell_label.img = self.empty_token if move not in valid_moves else self.valid_move

                cell_label.config(image=cell_label.img)

                human_move = False
                # If current player is human, and we're not moving through move history, we configure click
                #       events for cells corresponding to valid moves (and of course the game shouldn't be
                #       over in order to do it!)
                if not self.board.is_game_over() and self.current_player != 0 and isinstance(
                   self.players[self.current_player], HumanPlayer) and self.move_history_index == len(
                   self.all_moves):

                    human_move = True

                    # If human doesn't have a move, he has to pass
                    if len(valid_moves) == 0:
                        self.make_move_human(None, True)

                # Enable selecting the move by mouse for a human player
                if move in valid_moves and human_move:
                    cell_label.bind('<ButtonPress-1>', self.make_move_human)
                else:
                    cell_label.unbind('<ButtonPress-1>')

        if self.board.is_game_over():
            self.stop_timer = True
            
            black_score, white_score = self.board.get_final_score()
            game_over_message = 'Game Over!\n'
            if white_score == black_score:
                game_over_message += 'We have a tie!!!'
            else:
                game_over_message += '{} ({}) Wins the game!!!'.format(
                    self.players[BLACK] if black_score > white_score else self.players[WHITE],
                    Board.get_color_string(BLACK) if black_score > white_score else Board.get_color_string(WHITE))

            game_over_message += '\n\nFinal Score of the players:\n' + \
                                 'Black:      {}\n'.format(black_score) + \
                                 'White:     {}'.format(white_score)

            messagebox.showinfo(title='Game Over',
                                message=game_over_message)

            return

        # Update next and previous move buttons
        all_moves = len(self.all_moves)
        self.previous_move_button.config(state=DISABLED if self.move_history_index == 0 else NORMAL)
        self.next_move_button.config(
            state=DISABLED if self.move_history_index == all_moves or all_moves == 0 else NORMAL)

        # Update the turn color label
        if self.current_player == 0:
            self.turn_color_label.config(text='NONE', foreground='yellow')
        else:
            self.turn_color_label.config(
                text='{} ({})'.format(self.players[self.current_player], Board.get_color_string(self.current_player)),
                foreground='black' if self.current_player == BLACK else 'white')

        self.move_history_label.config(
            text='Total moves: {}{}'.format(len(self.all_moves),
                                            ' (Current Move: {})'.format(self.move_history_index)
                                            if self.move_history_index != all_moves and self.move_history_index != 0
                                            else ''))

        # The make-move button should be disabled in the following cases:
        #   *) We're moving through move history and we're not in the last move
        #   *) No players are configured
        #   *) Current player is a human player
        #   *) Game is over (of course!)
        self.make_move_button.config(state=DISABLED
                                     if self.move_history_index != all_moves or
                                     self.current_player == 0 or
                                     isinstance(self.players[self.current_player], HumanPlayer) or
                                     self.board.is_game_over()

                                     else NORMAL)

        # Display an instruction message based on make-move button's state:
        #   *) If it's disabled (and the game has started), player should click on one of the legal moves
        #   *) It it's enabled, we should click on it to make the computer move
        if 'disabled' not in self.make_move_button.state():
            self.last_move_label.config(text="Select 'Make Move' button to execute next move")
        elif len(self.players) > 0:
            self.last_move_label.config(text='Select your move by clicking one of the highlighted legal moves')

        # If current player is not human and we're not going through move history, make a move
        if self.current_player != 0 and \
                self.move_history_index == all_moves and \
                not isinstance(self.players[self.current_player], HumanPlayer):

            self.make_move()

        # Update last-move label
        self.last_move_label.configure(text='Last Move: {}'.format(
            'None' if self.last_move == tuple() or not self.game_started else '{} {}'.format(
                self.board.get_color_string(self.last_color),
                "to ' {} '".format(self.board.move_string(self.last_move))
                if self.last_move is not None
                else 'PASSED')))

    def start_game(self):
        if self.black_player_name.get() == '' or self.white_player_name.get() == '':
            messagebox.showerror(title='Missing Player Info',
                                 message='Please specify the name of both players')
            return

        self.players = dict()
        self.current_player = 0

        black_player_type = PlayerType(self.black_player_type.get())
        white_player_type = PlayerType(self.white_player_type.get())
        black_player_name = self.black_player_name.get()
        white_player_name = self.white_player_name.get()

        if black_player_type != PlayerType.human and white_player_type != PlayerType.human:
            messagebox.showerror(title='Player Type Error',
                                 message='At least one of the players should be a human player')
            return

        self.game_started = True
        self.start_timer()
        self.stop_timer = False

        self.players[BLACK] = create_player(black_player_type, black_player_name)
        self.players[WHITE] = create_player(white_player_type, white_player_name)

        self.current_player = BLACK

        # Enable and disable widgets accordingly
        self.start_game_button.config(state=DISABLED)
        self.black_player_name_entry.config(state=DISABLED)
        self.black_player_type_combo.config(state=DISABLED)
        self.white_player_name_entry.config(state=DISABLED)
        self.white_player_type_combo.config(state=DISABLED)
        self.reset_button.config(state=NORMAL)
        self.update()

    def update_level_spinbox(self, event, color):
        if color == BLACK:
            self.black_level_spin.configure(state=DISABLED if event.widget.get() == 'Human' else NORMAL)
        elif color == WHITE:
            self.white_player_level_spin.configure(state=DISABLED if event.widget.get() == 'Human' else NORMAL)

    def reset_players(self):
        self.black_player_type.set(PlayerType.human.value)
        self.white_player_type.set(PlayerType.human.value)
        self.black_player_name.set('')
        self.white_player_name.set('')
        self.players = []
        self.current_player = 0

    def reset_game(self):
        if not messagebox.askyesno(title='Confirm Reset',
                                   message='Are you sure you want to reset the game?'):
            return

        self.game_started = False
        self.stop_timer = True

        # Enable and disable widgets accordingly
        self.black_player_name_entry.config(state=NORMAL)
        self.black_player_type_combo.config(state=NORMAL)
        self.white_player_name_entry.config(state=NORMAL)
        self.white_player_type_combo.config(state=NORMAL)
        self.start_game_button.config(state=NORMAL)
        self.reset_button.config(state=DISABLED)
        self.white_player_level_spin.configure(state=DISABLED)
        self.black_level_spin.configure(state=DISABLED)
        self.timer_label.configure(text='')

        self.reset_players()
        self.board = Board()
        self.all_moves = []
        self.last_move = tuple()
        self.last_color = 0
        self.move_history_index = 0
        self.update()

    def start_timer(self):
        self.timer_label.config(text='Time Remaining: {}'.format(self.time_out_value.get()))
        self.timer_label.after(1000, self.display_timer)

    def display_timer(self):
        if self.stop_timer:
            return

        current_value = int(str(self.timer_label.cget('text')).split(': ')[1])
        if current_value == 1:
            self.timer_label.config(text='Time Remaining: 0')
            self.last_color = self.current_player
            self.last_move = None
            self.execute_move()

            if not self.board.is_game_over():
                self.start_timer()

        else:
            self.timer_label.config(text='Time Remaining: {}'.format(current_value - 1))
            self.timer_label.after(1000, self.display_timer)

    def change_turn(self):
        self.current_player *= -1

    def check_move_thread(self):
        if self.move_thread.is_alive():
            self.master.after(20, self.check_move_thread)
        else:
            self.progress_bar.stop()

    def make_move_human(self, event, force=False):
        if force:
            messagebox.showinfo(title='No Valid Move',
                                message="There's no valid move! You have to pass!")
        next_move = (event.widget.row, event.widget.column) if not force else None
        self.last_move = next_move
        self.last_color = self.current_player
        self.execute_move()

    def make_move(self):
        self.move_thread = threading.Thread(target=self.get_move)
        self.move_thread.daemon = True
        self.make_move_button.config(state=DISABLED)
        self.progress_bar.start()
        self.move_thread.start()
        self.master.after(20, self.check_move_thread)

    def get_move(self):
        current_player = self.players[self.current_player]
        player_level = self.black_player_level.get() if self.current_player == BLACK else self.white_player_level.get()
        next_move, value = current_player.get_best_move(self.board, player_level, self.time_out_value.get())
        self.last_move = next_move
        self.last_color = self.current_player
        self.execute_move()

    def execute_move(self):
        self.all_moves.append(self.last_move)
        self.move_history_index += 1
        self.board = self.board.execute_move(self.last_move)
        self.change_turn()
        self.progress_bar.stop()
        self.update()

    def previous_move(self):
        self.move_history_index -= 1

        if self.move_history_index >= 0:
            self.go_to_move()

    def next_move(self):
        self.move_history_index += 1

        if self.move_history_index <= len(self.all_moves):
            self.go_to_move()

    def go_to_move(self):
        self.board = Board()
        self.current_player = self.board.get_turn()
        for i in range(self.move_history_index):
            self.board = self.board.execute_move(self.all_moves[i])
            self.change_turn()

        self.update()


def main():
    root = Tk()
    Othello(root)
    root.mainloop()


if __name__ == '__main__':
    main()
