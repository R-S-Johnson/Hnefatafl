from GameLogic import HnefataflBoard
from GameWindow import GameWindow

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
    
    def on_click(self, row, col, tags):
        """
        Initial handling of mouse presses
        """
        print(f"({row}, {col}) {tags}")
        
        if self.selected:
            # Move
            if tags[0][:5] == "space":
                if self.game.move_piece(target=self.selected_coord,
                                        dest=(row, col),
                                        valid_moves=self.valid_moves):
                    self.window.move_piece(target_tag=self.selected_tag,
                                           dest=(row, col))
                    for captured in self.game.last_captured:
                        self.window.remove_piece(captured)
                    self.turn = 1 if self.turn==2 else 2
            # Deselect
            elif tags[0] == "piece" and tags[1] == self.selected_tag:
                self.selected = False
            self.window.dehighlight_cells()
        else:
            if tags[0] == "piece":
                if tags[2] == self.turn:
                    self.selected = True
                    self.selected_coord = (row, col)
                    self.selected_tag = tags[1]
                    self.valid_moves = self.game.valid_moves((row, col))
                    self.window.highlight_cells(self.valid_moves)
    
## TESTING ##
if __name__ == "__main__":
    A = GameController()
    A.window.mainloop()
    