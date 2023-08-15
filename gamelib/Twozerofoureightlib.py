from itertools import cycle
import tkinter as tk
import random

class AutomatedPlayer:
    def __init__(self, game):
        self.game = game
        self.directions = cycle(["up", "down", "left", "right"])
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            self.move_random()

    def stop(self):
        self.running = False

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def move_random(self):
        if not self.running:
            return

        direction = next(self.directions)
        self.game.move(direction)
        if self.game.is_game_over():
            self.game.display_game_over()
            self.stop()
            print("Game Over")
        else:
            self.game.root.after(100, self.move_random)

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.root.geometry("400x550")

        self.board = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()

        self.tiles = []
        self.tile_colors = {
            0: "#CDC1B4",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E"
        }

        self.score = 0
        self.high_score = 0  # Initialize the high score

        self.game_over = False  # Add this line

        self.setup_ui()

    def key_pressed(self, event):
        if self.game_over:  # Check the game_over flag
            return
        
        if event.keysym == "Up":
            self.move("up")
        elif event.keysym == "Down":
            self.move("down")
        elif event.keysym == "Left":
            self.move("left")
        elif event.keysym == "Right":
            self.move("right")

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#BBADA0")
        self.canvas.pack()

        # Add scoreboard label
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16, "bold"))
        self.score_label.pack(pady=10, padx=10, anchor="w")

        # Add high score label
        self.high_score_label = tk.Label(self.root, text="High Score: 0", font=("Arial", 16, "bold"))
        self.high_score_label.pack(pady=10, padx=10, anchor="w")

        automated_player = AutomatedPlayer(self)
        #Automate player
        auto_mode_button = tk.Button(self.root, text="Auto Mode", command=automated_player.toggle)
        auto_mode_button.pack()

        for i in range(4):
            row_tiles = []
            for j in range(4):
                tile_value = self.board[i][j]
                color = self.tile_colors.get(tile_value, "#3C3A32")
                tile = self.canvas.create_rectangle(j * 100, i * 100, (j + 1) * 100, (i + 1) * 100, fill=color)
                text = "" if tile_value == 0 else str(tile_value)
                tile_text = self.canvas.create_text((j + 0.5) * 100, (i + 0.5) * 100, text=text, font=("Arial", 24, "bold"), fill="black")
                row_tiles.append((tile, tile_text))
            self.tiles.append(row_tiles)

        self.root.bind("<Key>", self.handle_key_event)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.pack()

        self.start()

    def handle_key_event(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right"):
            direction = event.keysym.lower()
            self.move(direction)
            if self.is_game_over():
                self.display_game_over()    
            else:
                self.add_new_tile()

    def display_game_over(self):
        self.clear_canvas()  # Clear previous "Game Over" text
        self.canvas.create_text(200, 200, text="Game Over", font=("Arial", 24, "bold"), fill="black", tags="game_over_text")  # Add the "game_over_text" tag
            

    def update_tiles(self):
        self.update_score()
        for i in range(4):
            for j in range(4):
                tile_value = self.board[i][j]
                color = self.tile_colors.get(tile_value, "#3C3A32")
                self.canvas.itemconfig(self.tiles[i][j][0], fill=color)
                text = "" if tile_value == 0 else str(tile_value)
                self.canvas.itemconfig(self.tiles[i][j][1], text=text)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def is_game_over(self):

        # Check for possible moves or fully populated grid
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.game_over = False
                    return False
                if i > 0 and self.board[i][j] == self.board[i - 1][j]:
                    self.game_over = False
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    self.game_over = False
                    return False
                if j > 0 and self.board[i][j] == self.board[i][j - 1]:
                    self.game_over = False
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    self.game_over = False
                    return False
        
        self.game_over = True
        return True


    def move(self, direction):
        moved = False

        if direction == "up":
            for j in range(4):
                new_col = [0] * 4
                new_col_idx = 0
                for i in range(4):
                    if self.board[i][j] != 0:
                        if new_col[new_col_idx] == 0:
                            new_col[new_col_idx] = self.board[i][j]
                        elif new_col[new_col_idx] == self.board[i][j]:
                            new_col[new_col_idx] *= 2
                            self.score += new_col[new_col_idx]  # Add the merged value to the score
                            new_col_idx += 1
                        else:
                            new_col_idx += 1
                            new_col[new_col_idx] = self.board[i][j]
                if new_col != [self.board[i][j] for i in range(4)]:
                    moved = True
                    for i in range(4):
                        self.board[i][j] = new_col[i]

        elif direction == "down":
            for j in range(4):
                new_col = [0] * 4
                new_col_idx = 3
                for i in range(3, -1, -1):
                    if self.board[i][j] != 0:
                        if new_col[new_col_idx] == 0:
                            new_col[new_col_idx] = self.board[i][j]
                        elif new_col[new_col_idx] == self.board[i][j]:
                            new_col[new_col_idx] *= 2
                            self.score += new_col[new_col_idx]  # Add the merged value to the score
                            new_col_idx -= 1
                        else:
                            new_col_idx -= 1
                            new_col[new_col_idx] = self.board[i][j]
                if new_col != [self.board[i][j] for i in range(4)]:
                    moved = True
                    for i in range(3, -1, -1):
                        self.board[i][j] = new_col[i]

        elif direction == "left":
            for i in range(4):
                new_row = [0] * 4
                new_row_idx = 0
                for j in range(4):
                    if self.board[i][j] != 0:
                        if new_row[new_row_idx] == 0:
                            new_row[new_row_idx] = self.board[i][j]
                        elif new_row[new_row_idx] == self.board[i][j]:
                            new_row[new_row_idx] *= 2
                            self.score += new_row[new_row_idx]  # Add the merged value to the score
                            new_row_idx += 1
                        else:
                            new_row_idx += 1
                            new_row[new_row_idx] = self.board[i][j]
                if new_row != self.board[i]:
                    moved = True
                    self.board[i] = new_row

        elif direction == "right":
            for i in range(4):
                new_row = [0] * 4
                new_row_idx = 3
                for j in range(3, -1, -1):
                    if self.board[i][j] != 0:
                        if new_row[new_row_idx] == 0:
                            new_row[new_row_idx] = self.board[i][j]
                        elif new_row[new_row_idx] == self.board[i][j]:
                            new_row[new_row_idx] *= 2
                            self.score += new_row[new_row_idx]  # Add the merged value to the score
                            new_row_idx -= 1
                        else:
                            new_row_idx -= 1
                            new_row[new_row_idx] = self.board[i][j]
                if new_row != self.board[i]:
                    moved = True
                    self.board[i] = new_row

        if moved:
            self.add_new_tile()
            self.update_tiles()

    def clear_canvas(self):
        self.canvas.delete("game_over_text")

    def reset_game(self):
        if self.score > self.high_score:
            self.high_score = self.score  # Update the high score
        self.score = 0  # Reset the score
        self.board = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_tiles()
        self.clear_canvas()

    def close_window(self):
        self.root.destroy()

    def start(self):
        self.root.mainloop()

