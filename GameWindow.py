import tkinter as tk

class GameWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        
        # Controller for passing along user input
        self.controller = controller

        # Constants
        self.board_size = 11  # 11x11 board
        self.square_size = 50  # Size of each square in pixels

        # Window
        self.canvas = tk.Canvas(self, width=self.board_size * self.square_size,
                                height=self.board_size * self.square_size)
        self.canvas.pack()
        
        # Board and tags for click access
        self.draw_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.canvas.tag_bind(f"space_{row}_{col}", "<Button-1>", self.on_click)
        
        # Add Pieces
        

    def draw_board(self):
        """
        Draws the game board at game start, tagging each cell
        for Tkinter integration for easy cell click selection
        """
        colors = ("white", "gray")
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="black",
                                             tags=f"space_{row}_{col}")
                

    def draw_piece(self, row, col, player):
        """
        Draw piece on board/canvas at location (row, col)
        """
        
    def on_click(self, event):
        """
        Passes row, col to controller
        to handle board interaction
        """
        