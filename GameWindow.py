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
        self.board_colors = ("white", "gray")
        self.draw_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.canvas.tag_bind(f"space_{row}_{col}", "<Button-1>", self.on_click)
                
        # Remember last highlighted
        self.last_highlighted = []
        
        # Add Pieces
        self.draw_pieces()
        
        # Restart button option: "R"
        self.bind("<R>", self.on_key_press)
        
        # Button to save last state in logs: "Ctrl+s"
        self.bind("<Control-s>", self.on_key_press)
        

    def draw_board(self):
        """
        Draws the game board at game start, tagging each cell
        for Tkinter integration for easy cell click selection
        """
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.board_colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="black",
                                             tags=f"space_{row}_{col}")
                
                
    def draw_pieces(self):
        """
        Draws the pieces for the start of game layout
        tagging each piece for click integration and access
        """
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
                                                    tags=("piece", f"piece_id{id}", f"{BOARD_START[row][col]}"))
                    id += 1
                    self.canvas.tag_bind(piece, "<Button-1>", self.on_click)
                elif BOARD_START[row][col] == 3:
                    king = self.canvas.create_oval(x0-5, y0-5, x1+5, y1+5,
                                                   fill="dark blue",
                                                   tags=("piece", "king"))
                    self.canvas.tag_bind(king, "<Button-1>", self.on_click)

        
    def on_click(self, event):
        """
        Passes row, col to controller
        to handle board interaction
        """
        row = event.y//self.square_size
        col = event.x//self.square_size
        self.controller.on_click(row, col, self.canvas.gettags("current"))
        
        
    def on_key_press(self, event):
        """
        Passes key press call to controller.
        """
        self.controller.on_key_press(event)
        
        
    def highlight_cells(self, cells):
        """
        Used when a piece is selected to
        display valid moves
        """
        for cell in cells:
            row, col = cell
            self.canvas.itemconfig(f"space_{row}_{col}", fill="gold")
        self.last_highlighted = cells
    
    
    def dehighlight_cells(self, cells=None):
        """
        Dehighlights cells
        can be done manually through cells input,
        but usually remembers last highlighted
        and dehighlights those
        """
        if self.last_highlighted != [] and cells == None:
            for cell in self.last_highlighted:
                row, col = cell
                self.canvas.itemconfig(f"space_{row}_{col}", fill=self.board_colors[(row + col) % 2])


    def move_piece(self, target_tag, dest):
        """
        Move piece visualization to match back end
        """
        dest_row, dest_col = dest
        x0 = dest_col * self.square_size + 10
        y0 = dest_row * self.square_size + 10
        x1 = x0 + self.square_size - 20
        y1 = y0 + self.square_size - 20
        
        if target_tag == 'king':
            self.canvas.coords(target_tag,
                               x0-5, y0-5, x1+5, y1+5)
        else:
            self.canvas.coords(target_tag,
                               x0, y0, x1, y1)
        
    
    def remove_piece(self, target):
        """
        Remove piece visualization after captured
        given (row, col)
        """
        row, col = target
        x = col*self.square_size + self.square_size//2
        y = row*self.square_size + self.square_size//2
        target_tag = self.canvas.find_closest(x, y)
        self.canvas.delete(target_tag)