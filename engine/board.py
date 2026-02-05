from engine.enums import Tile
from engine.pawn import Pawn

class Board:
    def __init__(self, rows=9, cols=5):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.pawns = {}
        self.dead_white = []
        self.dead_purple = []
        self.next_pid = 0
        self.next_white_display = 0
        self.next_purple_display = 0

    def add_pawn(self, i, j, color):
        pid = self.next_pid
        self.next_pid += 1

        if color == Tile.WHITE:
            display_id = self.next_white_display
            self.next_white_display += 1
        else:
            display_id = self.next_purple_display
            self.next_purple_display += 1

        pawn = Pawn(pid, display_id, i, j, color)
        self.pawns[pid] = pawn
        self.grid[i][j] = pid

    def remove_pawn(self, pid):
        pawn = self.pawns.pop(pid)
        self.grid[pawn.i][pawn.j] = None

        if pawn.color == Tile.WHITE:
            self.dead_white.append(pawn.display_id) 
        else:
            self.dead_purple.append(pawn.display_id)

    def move_pawn(self, pid, ni, nj):
        pawn = self.pawns[pid]

        target = self.grid[ni][nj]
        if target is not None:
            self.remove_pawn(target)

        self.grid[pawn.i][pawn.j] = None
        pawn.i, pawn.j = ni, nj
        self.grid[ni][nj] = pid

    def get_pawn_by_display(self, display_id, color):
        for pawn in self.pawns.values():
            if pawn.color == color and pawn.display_id == display_id:
                return pawn
        return None

    def possible_moves(self, pid):
        pawn = self.pawns[pid]
        moves = []

        if pawn.color == Tile.WHITE:
            d = 1 
        else:
            d = -1
        ni = pawn.i + d

        if 0 <= ni < self.rows:
            if self.grid[ni][pawn.j] is None:
                moves.append(("move", ni, pawn.j))

            # diagonal attacks
            for nj in [pawn.j - 1, pawn.j + 1]:
                if 0 <= nj < self.cols:
                    target = self.grid[ni][nj]
                    if target is not None and self.pawns[target].color != pawn.color:
                        moves.append(("attack", ni, nj))

        return moves

    def all_possible_moves(self, color):
        moves = []
        for pid, pawn in self.pawns.items():
            if pawn.color == color:
                for move in self.possible_moves(pid):
                    moves.append((pid, *move))
        return moves

    def nb_pawn(self, color):
        return sum(1 for p in self.pawns.values() if p.color == color)

    def all_blocked(self, color):
        for pid, pawn in self.pawns.items():
            if pawn.color == color and self.possible_moves(pid):
                return False
        return True

    def arrive(self, color):
        if color == Tile.WHITE:
            target_row = self.rows - 1
        else:
            target_row = 0
        for pawn in self.pawns.values():
            if pawn.color == color and pawn.i == target_row:
                return True
        return False

    def win(self, color):
        if color == Tile.WHITE:
            enemy = Tile.PURPLE 
        else:
            enemy = Tile.WHITE

        return (
            self.nb_pawn(enemy) == 0
            or self.arrive(color)
        )

    def setup_initial_position(self):
        for j in range(self.cols):
            self.add_pawn(0, j, Tile.WHITE)
            self.add_pawn(1, j, Tile.WHITE)
            self.add_pawn(self.rows - 1, j, Tile.PURPLE)
            self.add_pawn(self.rows - 2, j, Tile.PURPLE)
