from window import GameWindow
import tkinter as tk

class MainWindow(tk.Tk):
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        
        # Controller for passing along user input
        self.controller = controller

        # Gameboard constants
        self.board_size = 11  # 11x11 board
        self.square_size = 50  # Size of each square in pixels

        self.build_ui()

        ### Keyboard input bindings ###
        # Restart button option: "R"
        self.bind("<R>", self.on_key_press)        
        # Button to save last state in logs: "Ctrl+s"
        self.bind("<Control-s>", self.on_key_press)
        # Load state from debug-logs
        self.bind("<Control-L>", self.on_key_press)

    
    def build_ui(self):
        # Frame for organizing
        self.window = tk.Frame(self)
        self.window.pack()

        # Game board window
        self.canvas = GameWindow(self.window, self.controller,
                                 self.board_size, self.square_size,
                                 width=self.board_size * self.square_size,
                                 height=self.board_size * self.square_size)
        
        # Labels
        self.title_label = tk.Label(self.window, text="Hnefatafl")
        self.turn_label = tk.Label(self.window, text="Turn: Attacker")

        # Interact buttons
        self.restart_button = tk.Button(self.window, command=self.controller.restart,
                                       text="Restart (Shift+R)")
        
        # Grid organization
        self.canvas.grid(column=0, row=0,
                         columnspan=8, rowspan=3)
        self.title_label.grid(column=9, row=0)
        self.turn_label.grid(column=9, row=1)
        self.restart_button.grid(column=9, row=2)
        
        
    def turn_rotate(self, turn):
        """
        Sets turn label for turn swaps
        """
        turn_label = 'Attacker' if turn == 2 else 'Defender'
        self.turn_label.config(text=f"Turn: {turn_label}")
    
        
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
    
    def set_board(self, board):
        """
        Sets board look to match input 2d list
        """
        self.canvas.set_board(board)

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