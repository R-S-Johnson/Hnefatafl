import tkinter as tk

class GameWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        # Constants
        self.self.board_size = 11  # 11x11 board
        self.self.square_size = 50  # Size of each square in pixels
        self.colors = ("white", "gray")  # Alternating square colors

        # Window
        self.canvas = tk.Canvas(self, width=self.board_size * self.square_size, height=self.board_size * self.square_size)
        self.canvas.pack()


    def draw_board(self, board):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

