import numpy as np

class HnefataflBoard:
    def __init__(self):
        # Board representation
        self.grid = [[0 for _ in range(11)] for _ in range(11)]
        self.board_size = 11

        # Invalid spaces for Pawns
        self.king_space = (5, 5)
        self.escape_spaces = [(0, 0), (10, 0), (0, 10), (10, 10)]

        # Piece Labels
        self.defend_pawn = 1
        self.attack_pawn = 2
        self.king = 3
        self.captured = []

        self.setup()

    def setup(self):
        self.grid = np.array([
            [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
            [2, 2, 0, 1, 1, 3, 1, 1, 0, 2, 2],
            [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0]
            ], dtype=int)
            
    def valid_moves(self, target, king=False):
        """
        Returns a list of tuple coordinates
        that equal all valid moves from input target
        king=True if King Piece is selected
        """
        valid_moves = []

        row = target[0]
        col = target[1]

        # If piece exists
        if self.grid[row, col] != 0:
            # Left
            board_chunk = self.grid[row, :col][::-1]
            for n, space in np.ndenumerate(self.grid[row, :col][::-1]):
                n, = n
                if space != 0:
                    valid_moves += [(row, i) for i in range(col-n, col)]
                    break
                if (n + 1) == len(board_chunk):
                    valid_moves += [(row, i) for i in range(col-n-1, col)]
            # Right
            board_chunk = self.grid[row, col+1:]
            for n, space in np.ndenumerate(self.grid[row, col+1:]):
                n, = n
                if space != 0:
                    valid_moves += [(row, i) for i in range(col+1, col+n+1)]
                    break
                if (n + 1) == len(board_chunk):
                    valid_moves += [(row, i) for i in range(col+1, col+n+2)]
            # Up
            board_chunk = self.grid[:row, col][::-1]
            for n, space in np.ndenumerate(self.grid[:row, col][::-1]):
                n, = n
                if space != 0:
                    valid_moves += [(i, col) for i in range(row-n, row)]
                    break
                if (n + 1) == len(board_chunk):
                    valid_moves += [(i, col) for i in range(row-n-1, row)]
            # Down
            board_chunk = self.grid[row+1:, col]
            for n, space in np.ndenumerate(self.grid[row+1:, col]):
                n, = n
                if space != 0:
                    valid_moves += [(i, col) for i in range(row+1, row+n+1)]
                    break
                if (n + 1) == len(board_chunk):
                    valid_moves += [(i, col) for i in range(row+1, row+n+2)]

        # Remove unusable spaces
        if self.king_space in valid_moves and not king:
            valid_moves.remove(self.king_space)
        for space in self.escape_spaces:
            if space in valid_moves:
                valid_moves.remove(space)

        return valid_moves
    
    def move_piece(self, target, location):
        """
        Checks validity of target and location,
        once validated, grid is modified and a
        capture is checked.
        Returns None if invalid target or location
        """
        if self.grid[target[0], target[1]] != 0:
            # Piece exists
            pass
        return None
    

## TESTING ##
if __name__ == "__main__":
    A = HnefataflBoard()
    print(A.valid_moves((5, 4)))