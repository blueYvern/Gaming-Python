import tkinter as tk
from tkinter import ttk
from gamelib.Tictaclib import GameBoard

def launch_tic_tac_toe():
    game_board = GameBoard()
    game_board.start()

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

    # You can add more buttons for other games here
    
    root.mainloop()

if __name__ == "__main__":
    main_menu()
