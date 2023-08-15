import tkinter as tk
from tkinter import ttk
from gamelib.Tictaclib import GameBoard
from gamelib.Twozerofoureightlib import AutomatedPlayer, Game2048

def launch_tic_tac_toe():
    game_board = GameBoard()
    game_board.start()

def launch_2048():
    game_2048 = Game2048()
    
    game_2048.start()
    # Implement the 2048 game interface using tkinter here

def main_menu():
    root = tk.Tk()
    root.title("Game Menu")
    root.geometry("400x300")  # Set the initial window size
    
    label = tk.Label(root, text="Choose a game to play:", font=('Arial', 18))
    label.pack(pady=20)
    
    button_style = ttk.Style()
    button_style.configure("GameButton.TButton", font=('Arial', 14), padding=10)
    
    tic_tac_toe_button = ttk.Button(root, text="Tic Tac Toe", command=launch_tic_tac_toe, style="GameButton.TButton")
    tic_tac_toe_button.pack()

    game_2048_button = ttk.Button(root, text="2048", command=launch_2048, style="GameButton.TButton")
    game_2048_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main_menu()
