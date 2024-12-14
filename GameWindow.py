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
        
        # Board and tags for mouse 1 events
        self.draw_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.canvas.tag_bind(f"space_{row}_{col}", "<Button-1>", self.on_click)
        
        # Add Pieces
        BOARD_START = [[0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                       [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
                       [2, 2, 0, 1, 1, 3, 1, 1, 0, 2, 2],
                       [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
                       [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                       [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0]]
        id = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                x0 = col * self.square_size + 10
                y0 = row * self.square_size + 10
                x1 = x0 + self.square_size - 20
                y1 = y0 + self.square_size - 20
                if BOARD_START[row][col] != 0 and BOARD_START[row][col] != 3:
                    piece = self.canvas.create_oval(x0, y0, x1, y1,
                                                    fill="red" if BOARD_START[row][col]==2 else "blue",
                                                    tags=("piece", f"{BOARD_START[row][col]}", f"piece_id{id}"))
                    id += 1
                    self.canvas.tag_bind(piece, "<Button-1>", self.on_click)
                elif BOARD_START[row][col] == 3:
                    king = self.canvas.create_oval(x0-5, y0-5, x1+5, y1+5,
                                                   fill="dark blue",
                                                   tags=("piece", "king"))
                    self.canvas.tag_bind(king, "<Button-1>", self.on_click)

    def draw_board(self):
        """
        Draws the game board at game start, tagging each cell
        for Tkinter integration for easy cell click selection
        """
        colors = ("white", "gray")
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="black",
                                             tags=f"space_{row}_{col}")
                
        
    def on_click(self, event):
        """
        Passes row, col to controller
        to handle board interaction
        """
        row = event.y//self.square_size
        col = event.x//self.square_size
        self.controller.on_click(row, col, self.canvas.gettags("current"))