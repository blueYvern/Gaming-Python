import tkinter as tk

class GameBoard:
    WINNING_COLOR = 'green'
    def __init__(self):
        self.game_board = tk.Tk()
        self.play_area = None
        self.cell_buttons = []
        self.reset_button = None
        self.status_label = ""
        self.game_disabled = False
        self.cell_value = "X"

        self.winning_cases = [
            ((1, 1), (1, 2), (1, 3)),
            ((2, 1), (2, 2), (2, 3)),
            ((3, 1), (3, 2), (3, 3)),
            ((1, 1), (2, 1), (3, 1)),
            ((1, 2), (2, 2), (3, 2)),
            ((1, 3), (2, 3), (3, 3)),
            ((1, 1), (2, 2), (3, 3)),
            ((3, 1), (2, 2), (1, 3))
        ]

        self.__create_game_board__()

    def __create_game_board__(self):
        gb = self.game_board
        gb.resizable(False, False)
        gb.title("Tic Tac Toe")
        gb.configure(bg='black')

        # Game title
        tk.Label(gb, text="--Tic Tac Toe--", font=('Arial', 25), foreground='white', bg='black').pack()

        # Player turn/status label
        self.status_label = tk.Label(gb, text="X's turn", font=('Arial', 15), bg='grey', fg='snow')
        self.status_label.pack(fill=tk.X)

        # Play area
        self.play_area = tk.Frame(gb, width=300, height=300, bg='black')
        self.play_area.pack(padx=10, pady=10)

        # Reset button
        self.reset_button = tk.Button(gb, text="Reset", command=self.__reset_game__, state=tk.DISABLED,
                                      font=('Arial', 12), bg='gray', fg='white')
        self.reset_button.pack(pady=5)

        # Initialize cell buttons
        for x in range(3):
            row_buttons = []
            for y in range(3):
                cell_button = tk.Button(self.play_area, text="", height=5, width=10, bg='black',
                                        command=lambda x=x, y=y: self.__set_cell__(x, y))
                cell_button.grid(row=x, column=y)
                row_buttons.append(cell_button)
            self.cell_buttons.append(row_buttons)

    def __set_cell__(self, x, y):
        if not self.game_disabled and self.cell_buttons[x][y].cget("text") == "":
            self.cell_buttons[x][y].configure(text=self.cell_value, bg='white', fg='black')

            if self.cell_value == "X":
                self.cell_value = "O"
                self.status_label.configure(text="O's turn")
            else:
                self.cell_value = "X"
                self.status_label.configure(text="X's turn")
            self.__check_winner__()
            self.cell_buttons[x][y].configure(state=tk.DISABLED)

    def __check_winner__(self):
        if self.__validate_win__("X"):
            self.status_label.configure(text="X won!")
            self.__highlight_winning_cells__("X")
            self.__disable_game__()
        elif self.__validate_win__("O"):
            self.status_label.configure(text="O won!")
            self.__highlight_winning_cells__("O")
            self.__disable_game__()
        elif all(self.cell_buttons[x][y].cget("text") != "" for x in range(3) for y in range(3)):
            self.status_label.configure(text="Draw!")
            self.__disable_game__()
            self.reset_button.configure(state=tk.NORMAL)  # Enable the reset button


    def __validate_win__(self, player):
        player_symbol = "X" if player == "X" else "O"
        for winning_cells in self.winning_cases:
            if all(self.cell_buttons[x - 1][y - 1].cget("text") == player_symbol for x, y in winning_cells):
                return True
        return False

    def __disable_game__(self):
        self.game_disabled = True
        self.reset_button.configure(state=tk.NORMAL)

    def __reset_game__(self):
        self.game_disabled = False
        self.x_cells = []
        self.o_cells = []
        self.cell_value = "X"
        self.status_label.configure(text="X's turn")
        self.reset_button.configure(state=tk.DISABLED)  # Disable the reset button

        for x in range(3):
            for y in range(3):
                self.cell_buttons[x][y].configure(text="", state=tk.NORMAL, bg='black')

    def __highlight_winning_cells__(self, player):
        player_symbol = "X" if player == "X" else "O"
        for winning_cells in self.winning_cases:
            if all(self.cell_buttons[x - 1][y - 1].cget("text") == player_symbol for x, y in winning_cells):
                for x, y in winning_cells:
                    self.cell_buttons[x - 1][y - 1].configure(bg=self.WINNING_COLOR)
                break  # Stop checking once we've found the winning cells


    def start(self):
        self.game_board.mainloop()
