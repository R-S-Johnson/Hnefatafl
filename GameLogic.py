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
        
    def capture_piece(self, target):
        if self.grid[target] != 0:
            self.captured.append(self.grid[target])
            self.grid[target] = 0
            
    def move_piece(self, target, dest):
        """
        Checks validity of target and dest,
        once validated, grid is modified and a
        capture is checked.
        Returns False if invalid target or dest,
        True if the piece successfully moved
        """
        if self.grid[target[0], target[1]] != 0:
            # Piece exists
            if dest in self.valid_moves(target):
                self.grid[dest] = self.grid[target]
                self.grid[target] = 0

                for captured in self.capture_check(dest):
                    self.capture_piece(captured)
                
                return True
        return False
    
    def capture_check(self, target):
        """
        target: location of newly moved piece
        Returns: list - location(s) of captured piece(s)
        """
        captured = []
        
        player = self.grid[target]
        op_player = 1 if player==0 else 0
        row = target[0]
        col = target[1]
        
        # Left
        if col > 1 and self.grid[row,col-1] == op_player:
            esc_king_space = (row,col-2) == (0,0) or (row,col-2) == (10,0) or (row,col-2) == (5,5)
            if self.grid[row,col-2] == player or esc_king_space:
                captured.append((row,col-1))
        # Right
        if col < self.board_size-2 and self.grid[row,col+1] == op_player:
            esc_king_space = (row,col+2) == (10,0) or (row,col+2) == (10,10) or (row,col+2) == (5,5)
            if self.grid[row,col+2] == player or esc_king_space:
                captured.append((row,col+1))
        # Up
        if row > 1 and self.grid[row-1,col] == op_player:
            esc_king_space = (row-2,col) == (0,0) or (row-2,col) == (0,10) or (row-2,col) == (5,5)
            if self.grid[row-2,col] == player or esc_king_space:
                captured.append((row-1,col))         
        # Down
        if row < self.board_size-2 and self.grid[row+1,col] == op_player:
            esc_king_space = (row+2,col) == (10,0) or (row+2,col) == (10,10) or (row+2,col) == (5,5)
            if self.grid[row+2,col] == player or esc_king_space:
                captured.append((row+1,col))
        
        return captured


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
    
    

## TESTING ##
if __name__ == "__main__":
    A = HnefataflBoard()
    print(A.valid_moves((5, 4)))