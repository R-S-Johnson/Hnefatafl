from GameLogic import HnefataflBoard
from GameWindow import GameWindow

class GameController:
    def __init__(self):
        self.game = HnefataflBoard()
        self.window = GameWindow(self)
    
    
    
## TESTING ##
if __name__ == "__main__":
    A = GameController()
    A.window.mainloop()