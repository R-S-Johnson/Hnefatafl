from GameLogic import HnefataflBoard
from GameWindow import GameWindow
import json

class GameController:
    def __init__(self):
        self.game = HnefataflBoard()
        self.window = GameWindow(self)
        
        # True if a piece is selected
        self.selected = False
        self.selected_coord = ()
        self.selected_tag = None
        
        # Turn tracker: 1 = Defender, 2 = Attacker
        self.turn = 2
        
        # Memory of last set of valid moves
        self.valid_moves = []
        
        # Memory of last player action
        self.last_action = []
        
        # Track GameOver state
        self.game_over = False
        self.winner = None
        
        
    def restart(self):
        """
        Resets aspects of game state
        to init values
        """
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.grid[(row, col)] != 0:
                    self.window.remove_piece((row, col))
        self.window.draw_pieces()
        self.game = HnefataflBoard()
        self.turn = 2
        self.game_over = False
        self.winner = None
        self.selected = False
        
    
    def on_click(self, row, col, tags):
        """
        Handling of mouse press events
        """
        print(f"({row}, {col}) {tags}")
        self.last_action = [row, col, tags]
        
        if self.selected:
            self.selected_options(tags, row, col)
        else:
            self.unselected_options(tags, row, col)     
        # Edit GameOver state based on win conditions
        win_cond = self.game.win_conditions()
        if win_cond != 0:
            self.game_over = True
            self.winner = win_cond
    
    
    def on_key_press(self, event):
        """
        Handling of key press events
        "R": Restart
        "Ctrl+s": Log last state
        """
        print(event.state, event.keysym, event.keycode)
        
        # Restart
        if event.char == event.keysym == "R":
            self.restart()
        # Log last states
        elif (event.state & 0x4) and event.keysym == "s":
            self.log_last_turn()
    
    
    def selected_options(self, tags, row, col):
        """
        Inacts game state changes based on
        player input and the fact that a piece
        is selected
        """
        # Expect move or deselect
        if tags[0][:5] == "space":
            # If piece move is successful
            if self.game.move_piece(target=self.selected_coord,
                                    dest=(row, col),
                                    valid_moves=self.valid_moves):
                self.window.move_piece(target_tag=self.selected_tag,
                                        dest=(row, col))
                # Remove captured pieces
                for captured in self.game.last_captured:
                    self.window.remove_piece(captured)
                # Turn rotate, deselect piece
                self.turn = 1 if self.turn==2 else 2
                self.selected = False
                self.window.dehighlight_cells()
        # Deselect
        elif tags[0] == "piece" and tags[1] == self.selected_tag:
            self.selected = False
            self.window.dehighlight_cells()
    
    
    def unselected_options(self, tags, row, col):
        """
        Inacts game state changes based on
        player input and the fact that a piece
        is NOT selected
        """
        # Expected piece input to select
        if tags[0] == "piece":
            if tags[1] == "king" and self.turn == 1:
                self.selected = True
                self.selected_coord = (row, col)
                self.selected_tag = "king"
                self.valid_moves = self.game.valid_moves((row, col),
                                                            king=True)
                self.window.highlight_cells(self.valid_moves)
            elif int(tags[2]) == self.turn:
                self.selected = True
                self.selected_coord = (row, col)
                self.selected_tag = tags[1]
                self.valid_moves = self.game.valid_moves((row, col))
                self.window.highlight_cells(self.valid_moves)
                
    
    def log_last_turn(self):
        """
        Saves last turn (board state, player action,
        general memory dump)
        """
        log = {
            "board-state": self.game.grid.tolist(),
            "player-action": self.last_action,
            "memory-dump": {
                "selected-info": {"selected": self.selected,
                                  "selected-coord": self.selected_coord,
                                  "tag": self.selected_tag},
                "turn": self.turn,
                "game-over-state": {"game-over": self.game_over,
                                    "winner": self.winner},
                "captured-info": {f"last-captured": self.game.last_captured,
                                  "king-captured": self.game.king_captured},
                "last-highlighted": self.window.last_highlighted
            }
        }
        with open("debug-logs/log-last-turn", 'w') as f:
            json.dump(log, f, indent=4)

    
if __name__ == "__main__":
    A = GameController()
    A.window.mainloop()
    