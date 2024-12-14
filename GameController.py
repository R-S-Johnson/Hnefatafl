from GameLogic import HnefataflBoard
from GameWindow import GameWindow

class GameController:
    def __init__(self):
        self.game = HnefataflBoard()
        self.window = GameWindow(self)
        
        # True if a piece is selected
        self.selected = False
        self.selected_coord = ()
        
        # Turn tracker: 1 = Defender, 2 = Attacker
        self.turn = 2
        
        # Memory of last set of valid moves
        self.valid_moves = []
    
    def on_click(self, row, col, tags):
        """
        Initial handling of mouse presses
        """
        print(f"({row}, {col}) {tags}")
        
        # Space or piece
    
## TESTING ##
if __name__ == "__main__":
    A = GameController()
    A.window.mainloop()