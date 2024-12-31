import tkinter as tk

class GameWindow(tk.Canvas):
        
    def __init__(self, parent, controller, board_size, square_size, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Game controller for user input
        self.controller = controller

        # Gameboard constants
        self.board_size = board_size
        self.square_size = square_size

        # Board and tags for mouse 1 events
        self.board_colors = ("white", "gray")
        self.draw_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.tag_bind(f"space_{row}_{col}", "<Button-1>", self.on_click)
                
        # Remember last highlighted
        self.last_highlighted = []
        
        # Add Pieces
        self.draw_pieces()
            

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
                self.create_rectangle(x1, y1, x2, y2,
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
                if BOARD_START[row][col] != 0:
                    self.draw_piece(row, col, BOARD_START[row][col], id)
                    if BOARD_START[row][col] != 3:
                        id += 1
                        

    def draw_piece(self, row, col, tag, id):
        """
        Draws piece at row, col
        based on player tag
        """
        x0 = col * self.square_size + 10
        y0 = row * self.square_size + 10
        x1 = x0 + self.square_size - 20
        y1 = y0 + self.square_size - 20
        if tag != 3:
            piece = self.create_oval(x0, y0, x1, y1,
                                            fill="red" if tag==2 else "blue",
                                            tags=("piece", f"piece_id{id}", f"{tag}"))
            self.tag_bind(piece, "<Button-1>", self.on_click)
        elif tag == 3:
            king = self.create_oval(x0-5, y0-5, x1+5, y1+5,
                                            fill="dark blue",
                                            tags=("piece", "king"))
            self.tag_bind(king, "<Button-1>", self.on_click)


    def set_board(self, board):
        """
        Sets board look to match input 2d list
        """
        self.delete("piece")
        id = 0
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] != 0:
                    self.draw_piece(row, col, board[row][col], id)
                    id += 1

        
    def on_click(self, event):
        """
        Passes row, col, and tags
        to parent to handle board interaction
        """
        row = event.y//self.square_size
        col = event.x//self.square_size
        self.controller.on_click(row, col, self.gettags("current"))
                
        
    def highlight_cells(self, cells):
        """
        Used when a piece is selected to
        display valid moves
        """
        for cell in cells:
            row, col = cell
            self.itemconfig(f"space_{row}_{col}", fill="gold")
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
                self.itemconfig(f"space_{row}_{col}", fill=self.board_colors[(row + col) % 2])


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
            self.coords(target_tag,
                               x0-5, y0-5, x1+5, y1+5)
        else:
            self.coords(target_tag,
                               x0, y0, x1, y1)
        
    
    def remove_piece(self, target):
        """
        Remove piece visualization after captured
        given (row, col)
        """
        row, col = target
        x = col*self.square_size + self.square_size//2
        y = row*self.square_size + self.square_size//2
        target_tag = self.find_closest(x, y)
        self.delete(target_tag)