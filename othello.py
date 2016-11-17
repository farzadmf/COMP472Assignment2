from tkinter import *
from tkinter import ttk
from player import *
import threading
from time import *
from tkinter import messagebox


class Othello:
    def __init__(self, master: Tk):

        master.title('Othello (Reversi) Game')
        master.resizable(False, False)

        self.master = master  # type: Tk
        self.move_thread = threading.Thread()
        self.board = Board()  # type: Board
        self.last_move = tuple()  # type: tuple
        self.all_moves = []
        self.move_history_index = 0

        # ++++++++++++++++++++++++++++++ Frames ++++++++++++++++++++++++++++++++++
        # Header frame
        self.header_frame = ttk.Frame(master)
        self.header_frame.pack(padx=10, pady=10)

        # Frame containing buttons
        self.buttons_frame = ttk.Frame(self.header_frame)
        self.buttons_frame.pack()

        # Frame for configuring players
        self.players_frame = ttk.Frame(self.header_frame)
        self.players_frame.pack(fill=X, padx=10, pady=10)

        # Content frame containing game and table
        self.content_frame = ttk.Frame(master)
        self.content_frame.pack()

        # Frames containing letters
        self.left_numbers = ttk.Frame(self.content_frame)
        self.right_numbers = ttk.Frame(self.content_frame)
        self.left_numbers.grid(row=1, column=0)
        self.right_numbers.grid(row=1, column=2)

        # Frames containing numbers
        self.top_letters = ttk.Frame(self.content_frame)
        self.bottom_letters = ttk.Frame(self.content_frame)
        self.top_letters.grid(row=0, column=1)
        self.bottom_letters.grid(row=2, column=1)

        # Frame containing the game
        self.game_frame = ttk.Frame(self.content_frame)
        self.game_frame.grid(row=1, column=1)

        # Footer frame
        self.footer_frame = ttk.Frame(master)
        self.footer_frame.pack(fill=X, padx=10, pady=10)
        # ------------------------------------------------------------------------

        # ++++++++++++++++++++++ Images and Icons ++++++++++++++++++++++++++++++++
        # Images for cells
        self.black_token = PhotoImage(file='Images/black_small.gif')
        self.white_token = PhotoImage(file='Images/white_small.gif')
        self.empty_token = PhotoImage(file='Images/empty_small.gif')
        self.last_move_black = PhotoImage(file='Images/last_move_black.gif')
        self.last_move_white = PhotoImage(file='Images/last_move_white.gif')
        self.valid_move = PhotoImage(file='Images/valid_move2.gif')

        # Images for the table
        self.letters = [None] * 8
        self.numbers = [None] * 8
        self.letters[0] = PhotoImage(file='Images/A.gif')
        self.letters[1] = PhotoImage(file='Images/B.gif')
        self.letters[2] = PhotoImage(file='Images/C.gif')
        self.letters[3] = PhotoImage(file='Images/D.gif')
        self.letters[4] = PhotoImage(file='Images/E.gif')
        self.letters[5] = PhotoImage(file='Images/F.gif')
        self.letters[6] = PhotoImage(file='Images/G.gif')
        self.letters[7] = PhotoImage(file='Images/H.gif')
        self.numbers[0] = PhotoImage(file='Images/1.gif')
        self.numbers[1] = PhotoImage(file='Images/2.gif')
        self.numbers[2] = PhotoImage(file='Images/3.gif')
        self.numbers[3] = PhotoImage(file='Images/4.gif')
        self.numbers[4] = PhotoImage(file='Images/5.gif')
        self.numbers[5] = PhotoImage(file='Images/6.gif')
        self.numbers[6] = PhotoImage(file='Images/7.gif')
        self.numbers[7] = PhotoImage(file='Images/8.gif')

        # Icons for buttons
        self.next_icon = PhotoImage(file='Images/next.gif')
        self.previous_icon = PhotoImage(file='Images/previous.gif')
        self.play_icon = PhotoImage(file='Images/play.gif')
        self.reset_icon = PhotoImage(file='Images/reset.gif')
        # ------------------------------------------------------------------------

        # TODO: temporary widgets
        self.make_move_button = ttk.Button(self.buttons_frame, text='Make Move', command=lambda: self.make_move())
        self.make_move_button.img = self.play_icon
        self.make_move_button.config(image=self.make_move_button.img, compound=LEFT)
        self.make_move_button.pack(side=LEFT, padx=10)

        self.reset_button = ttk.Button(self.buttons_frame, text='Reset Game', command=lambda: self.reset_game())
        self.reset_button.img = self.reset_icon
        self.reset_button.config(image=self.reset_button.img, compound=LEFT)
        self.reset_button.pack(side=LEFT, padx=40)

        self.previous_move_button = ttk.Button(self.buttons_frame, text='Previous Move',
                                               command=lambda: self.previous_move())
        self.previous_move_button.img = self.previous_icon
        self.previous_move_button.config(image=self.previous_move_button.img, compound=LEFT)
        self.previous_move_button.pack(side=LEFT, padx=10)

        self.next_move_button = ttk.Button(self.buttons_frame, text='Next Move', command=lambda: self.next_move())
        self.next_move_button.img = self.next_icon
        self.next_move_button.config(image=self.next_move_button.img, compound=LEFT)
        self.next_move_button.pack(side=LEFT, padx=10)

        ttk.Button(self.buttons_frame, text='Test Button', command=lambda: self.test_me()).pack(side=LEFT, padx=10)

        # +++++++++++++++++++++++++ Configure players ++++++++++++++++++++++++++++
        # Controls for configuring players
        self.black_player_name = StringVar()
        self.white_player_name = StringVar()
        self.black_player_type = StringVar()
        self.white_player_type = StringVar()

        # Default player types
        self.black_player_type.set(PlayerType.human.value)
        self.white_player_type.set(PlayerType.human.value)

        # Black player configuration frame and controls
        self.black_player_frame = ttk.LabelFrame(self.players_frame, text='Black Player Config')
        self.black_player_frame.pack(side=LEFT)
        ttk.Label(self.black_player_frame, text='Name: ').grid(row=0, column=0, sticky='e')
        self.black_player_name_entry = ttk.Entry(self.black_player_frame, width=20,
                                                 textvariable=self.black_player_name)
        self.black_player_name_entry.grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(self.black_player_frame, text='Type: ').grid(row=1, column=0, sticky='e')
        self.black_player_type_combo = ttk.Combobox(
            self.black_player_frame,
            width=17,
            values=list(member.value for _, member in PlayerType.__members__.items()),
            textvariable=self.black_player_type)
        self.black_player_type_combo.grid(row=1, column=1, padx=5, sticky='w')

        # White player configuration frame and controls
        self.white_player_frame = ttk.LabelFrame(self.players_frame, text='White Player Config')
        self.white_player_frame.pack(side=LEFT, padx=20)
        ttk.Label(self.white_player_frame, text='Name: ').grid(row=0, column=0, sticky='e')
        self.white_player_name_entry = ttk.Entry(self.white_player_frame, width=20,
                                                 textvariable=self.white_player_name)
        self.white_player_name_entry.grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(self.white_player_frame, text='Type: ').grid(row=1, column=0, sticky='e')
        self.white_player_type_combo = ttk.Combobox(
            self.white_player_frame,
            width=17,
            values=list(member.value for _, member in PlayerType.__members__.items()),
            textvariable=self.white_player_type)
        self.white_player_type_combo.grid(row=1, column=1, padx=5, sticky='w')
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

        # TODO: temporary widgets
        self.turn_label = ttk.Label(self.footer_frame)
        self.turn_label.pack(fill=X)

        self.progress_bar = ttk.Progressbar(self.footer_frame, orient=HORIZONTAL)
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.pack(fill=X)

        self.time_label = ttk.Label(self.footer_frame)
        self.time_label.pack(fill=X, side=RIGHT)
        self.start_time()

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

        # Set up the players
        self.players = []
        self.current_player = -1

        # ++++++++++++++++++++++++++++++ Styles ++++++++++++++++++++++++++++++++++
        self.style = ttk.Style()

        # Change the background color for the game frame to black
        self.style.configure('GameFrame.TFrame', background='black')
        self.content_frame.config(style='GameFrame.TFrame')
        self.game_frame.config(style='GameFrame.TFrame')
        self.left_numbers.config(style='GameFrame.TFrame')
        self.right_numbers.config(style='GameFrame.TFrame')
        self.top_letters.config(style='GameFrame.TFrame')
        self.bottom_letters.config(style='GameFrame.TFrame')
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

                # TODO: this should be something that actually does something!!!
                if move in valid_moves:
                    cell_label.bind('<ButtonPress-1>', lambda event: print(
                        '{}'.format(Board.move_string((event.widget.row, event.widget.column)))))
                else:
                    cell_label.unbind('<ButtonPress-1>')

                cell_label.config(image=cell_label.img)

        # Update the turn label
        # TODO: do I need the number of flips???
        self.turn_label.config(text='Number of flips: {}       Current Player: {},     Total moves: {}'.format(
            self.board.get_last_flip_count(),
            'NONE' if self.current_player == -1 else self.players[self.current_player],
            len(self.all_moves)))

        # Update next and previous move buttons
        all_moves = len(self.all_moves)
        self.previous_move_button.config(state=DISABLED if self.move_history_index == 0 else NORMAL)
        self.next_move_button.config(
            state=DISABLED if self.move_history_index == all_moves or all_moves == 0 else NORMAL)

        # The make-move button should only be enabled when we go to the last move
        self.make_move_button.config(state=DISABLED if self.move_history_index != all_moves else NORMAL)

    # TODO: temporary function
    def test_me(self):
        for i in range(30):
            self.make_move_button.invoke()
            sleep(1)

    def start_time(self):
        self.time_label.config(text='5')
        self.display_time()

    def display_time(self):
        # now = strftime('%H:%M:%S')
        current_value = int(self.time_label.cget('text'))
        if current_value == 1:
            self.time_label.config(text='0')
            print("CHANGE TURN")
        else:
            self.time_label.config(text=str(current_value - 1))
            self.time_label.after(1000, self.display_time)

    def change_turn(self):
        self.current_player = (self.current_player + 1) % 2

    def reset_game(self):
        self.black_player_type.set(PlayerType.human.value)
        self.white_player_type.set(PlayerType.human.value)
        self.black_player_name.set('')
        self.white_player_name.set('')
        self.board = Board()
        self.all_moves = []
        self.last_move = tuple()
        self.move_history_index = 0
        self.update()

    def check_move_thread(self):
        if self.move_thread.is_alive():
            self.master.after(20, self.check_move_thread)
        else:
            self.progress_bar.stop()
            self.make_move_button.config(state=NORMAL)

    def make_move(self):
        if self.board.is_game_over():
            print('GAME OVER MAN!')
            self.board.print_statistics()
            return

        if len(self.players) != 2 or self.current_player == -1:
            messagebox.showerror(title='Insufficient Number of Players',
                                 message='You must select the two players to continue playing')
            return

        self.move_thread = threading.Thread(target=self.get_move)
        self.move_thread.daemon = True
        self.make_move_button.config(state=DISABLED)
        self.progress_bar.start()
        self.move_thread.start()
        self.master.after(20, self.check_move_thread)

    def get_move(self):
        current_player = self.players[self.current_player]
        next_move, value = current_player.get_best_move(self.board, 2)
        self.last_move = next_move
        self.all_moves.append(next_move)
        self.move_history_index += 1
        self.board = self.board.execute_move(next_move)
        self.change_turn()
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
        for i in range(self.move_history_index):
            self.board = self.board.execute_move(self.all_moves[i])

        self.update()


def main():
    root = Tk()
    Othello(root)
    root.mainloop()


if __name__ == '__main__':
    main()
