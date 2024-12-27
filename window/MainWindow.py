from window import GameWindow
import tkinter as tk

class MainWindow(tk.Tk):
    
    def __init__(self, controller):
        super().__init__()
        
        # Controller for passing along user input
        self.controller = controller

        # Gameboard constants
        self.board_size = 11  # 11x11 board
        self.square_size = 50  # Size of each square in pixels

        # Game window
        self.canvas = GameWindow(self, self.board_size, self.square_size,
                                 width=self.board_size * self.square_size,
                                 height=self.board_size * self.square_size)
        self.canvas.pack()

        # Restart button option: "R"
        self.bind("<R>", self.on_key_press)
        
        # Button to save last state in logs: "Ctrl+s"
        self.bind("<Control-s>", self.on_key_press)


    def on_board_click(self, row, col, tags):
        """
        Passes board click event to
        controller for handling
        """
        self.controller.on_click(row, col, tags)
        
 
    def on_key_press(self, event):
        """
        Passes key press event to
        controller for handling
        """
        self.controller.on_key_press(event)
        
    
    ## Methods passing board modification calls to GameWindow ##
    def draw_pieces(self):
        """
        Draws the pieces for the start of game layout
        tagging each piece for click integration and access
        """
        self.canvas.draw_pieces()    

    def highlight_cells(self, cells):
        """
        Used when a piece is selected to
        display valid moves
        """
        self.canvas.highlight_cells(cells)
    
    def dehighlight_cells(self, cells=None):
        """
        Dehighlights cells
        can be done manually through cells input,
        but usually remembers last highlighted
        and dehighlights those
        """
        self.canvas.dehighlight_cells(cells)
        
    def move_piece(self, target_tag, dest):
        """
        Move piece visualization to match back end
        """
        self.canvas.move_piece(target_tag, dest)

    def remove_piece(self, target):
        """
        Remove piece visualization after captured
        given (row, col)
        """
        self.canvas.remove_piece(target)