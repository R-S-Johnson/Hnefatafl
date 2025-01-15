The Viking Game, also known as Hnefatafl, is an abstract strategy board game that dates back to the Viking Age. It's uniqueness lies in its simple yet asymmetric gameplay. In it, one  player controls the attackers trying to capture the king, while the other controls the king and their defenders, aiming to lead the king to safety at the board’s corners.

### Start Command:
'''
python main.py
'''

# Main Goal
Simulate Hnefatafl such that the game can be played with 1 or 2 players. When played with 1 player a bot is enabled, powered by a machine learning algorithm. The hope is this ML alg could use pattern recognition, clustering, etc to develop overarching strategies, popular opening setups, etc for both the attacker side and the defender side.

Given how old this game is, different translations and version of the game, board, and rules exist. The hope is to eventually support more than just the "Viking Game" version.

## How to interact
After running the start command, a new game is set up and ready to play, attackers always go first. 13 Defender pieces (12 pawns and the king) are displayed in blue (the king is in the center and is larger) and 24 attackers (entirely pawns) in red. When a piece is clicked/selected all valid spaces to move are displayed in yellow. That piece must be de-selected to select a different piece. If a valid move is selected, the piece will move there and other pieces will be removed from the board if captured with that move. The "restart" button can be used to reset the game state to the beginning of the game (Shift+R shortcut).

### Command line arguments
The only cla integrated is a debug mode turned on with "--debug-mode". However this is unadvised without knowledge on the structure of the needed debug-logs folder and files.

## Game Instructions
All pieces (king and pawns) move in the same way: in straight lines along rows and columns. They can move any number of squares in one direction, but cannot jump over other pieces.
The 4 corners (where the king needs to escape to) and the center of the board are off limits to any pawns, however pawns **can** jump over the center tile if unocupied.
### Capturing
If a pawn moves next to an enemy pawn and there is a friendly pawn on the opposite side of the enemy pawn, that pawn is captured and removed from the board. Note that this does not work in reverse, if a pawn moves between 2 enemy pawns it is not captured. In addition to this, the center and corner spaces, if unocupied, act as enemy pawns to both attacker and defender pawns for the purpose of capturing. Capturing the king works differently and also ends the game
### Ending the Game
The defender wins if they move the king to one of the 4 corners of the board. The attacker wins if they capture the king, which requires attacker pawns to move to all 4 sides of the king, rendering it unable to move.
Once the game is over no more pieces can be moved and the simulation must be restarted.

## Machine Learning Backend
Currently no features exist here