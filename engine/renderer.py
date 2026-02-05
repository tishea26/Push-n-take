from rich.text import Text
from rich.console import Console
from engine.enums import Tile, COLORS

console = Console()

WHITE_BG = "black on #ffffff"
PURPLE_BG = "black on #c792ea"

def pawn_text(pawn):
    if pawn.color == Tile.WHITE:
        style = WHITE_BG
    else:
        style = PURPLE_BG
    return Text(f" {pawn.display_id} ", style=f"bold {style}")

def build_header(turn):
    t = Text()
    t.append("\n========== ", style=COLORS["cyan"])
    t.append("Push'n'takes", style="bold magenta")
    t.append(" ==========\n\n", style=COLORS["cyan"])

    t.append(" Tour : ", style=COLORS["yellow"])
    if turn == Tile.WHITE:
        t.append("WHITE\n\n", style=f"bold {COLORS["white"]}")
    else:
        t.append("PURPLE\n\n", style=f"bold {COLORS["purple"]}")

    return t

def draw_board(board):
    t = Text()
    t.append("    ", style=COLORS["cyan"])

    for j in range(board.cols):
        t.append(f" {j} ", style=COLORS["cyan"])
    t.append("\n")

    for i in range(board.rows):
        t.append(f"  {i} ", style=COLORS["cyan"])

        for j in range(board.cols):
            pid = board.grid[i][j]

            if pid is None:
                t.append(" . ", style="dim")
            else:
                pawn = board.pawns[pid]
                t.append_text(pawn_text(pawn))

        t.append("\n")

    t.append("\n")
    return t

def build_error(error_message):
    t = Text()
    if error_message:
        t.append(" ⚠ ERREUR : ", style=f"bold {COLORS["red"]}")
        t.append(error_message + "\n\n", style=COLORS["red"])
    return t

def build_dead(board):
    t = Text()
    t.append(" Pions capturés :\n", style=COLORS["yellow"])

    t.append("  WHITE :  ", style=f"bold {COLORS["white"]}")
    t.append(" ".join(map(str, board.dead_white)) or "-", style=COLORS["cyan"])
    t.append("\n")

    t.append("  PURPLE : ", style=f"bold {COLORS["purple"]}")
    t.append(" ".join(map(str, board.dead_purple)) or "-", style=COLORS["cyan"])
    t.append("\n\n")

    return t

def build_commands(turn):
    t = Text()
    if turn == Tile.PURPLE:
        t.append("Je réfléchis...\n\n")
        return t

    t.append("  [m <id>]", style=COLORS["cyan"])
    t.append("        Avancer\n", style=COLORS["blue"])

    t.append("  [a <id1> <id2>]", style=COLORS["cyan"])
    t.append(" Attaquer le pion <id2> avec le pion <id1>\n", style=COLORS["blue"])

    return t

def render(board,turn, error_message=None):
    console.clear()

    t = Text.assemble(
        build_header(turn),
        build_error(error_message),
        draw_board(board),
        build_dead(board),
        build_commands(turn)
    )

    console.print(t)
