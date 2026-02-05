from engine.board import Board
from engine.renderer import render
from engine.enums import Tile
from engine.ai import minimax
import time

def switch_turn(turn):
    if turn == Tile.WHITE:
        return Tile.PURPLE
    else:
        return Tile.WHITE

def parse_command(cmd):
    parts = cmd.strip().split()
    
    if len(parts) == 2 and parts[0].lower() == "m":
        try:
            return ("move", int(parts[1])), None
        except ValueError:
            return None, "invalid ID"

    if len(parts) == 3 and parts[0].lower() == "a":
        try:
            attacker_id = int(parts[1])
            target_id = int(parts[2])
            return ("attack", attacker_id, target_id), None
        except ValueError:
            return None, "invalid ID"

    return None, "invalid command"

def main():
    board = Board()
    board.setup_initial_position()

    turn = Tile.WHITE
    error_message = None
    depth = 3

    while True:
        render(board,turn, error_message)

        if board.all_blocked(Tile.WHITE) and board.all_blocked(Tile.PURPLE):
            print("It's a draw !")
            break
        if board.win(Tile.WHITE):
            print("WHITE wins !")
            break
        if board.win(Tile.PURPLE):
            print("PURPLE wins !")
            break

        if board.all_blocked(turn):
            error_message = f"{turn.name} is blocked and loses its turn."
            turn = switch_turn(turn)
            continue

        # Human turn
        if turn == Tile.WHITE:
            cmd = input("> ").strip()
            parsed, err = parse_command(cmd)
            if err:
                error_message = err
                continue

            if parsed is None:
                error_message = "invalid command."
                continue

            action = parsed[0]

            if action == "move":
                display_id = parsed[1]
                pawn = board.get_pawn_by_display(display_id, turn)
                if pawn is None:
                    error_message = f"No pawn with this ID: {display_id}"
                    continue

                moves = board.possible_moves(pawn.id)
                found = False
                for m in moves:
                    if m[0] == "move":
                        board.move_pawn(pawn.id, m[1], m[2])
                        found = True
                        break

                if not found:
                    error_message = f"The pawn {display_id} cannot move forward."
                    continue

            elif action == "attack":
                attacker_display = parsed[1]
                target_display = parsed[2]

                attacker = board.get_pawn_by_display(attacker_display, turn)
                if attacker is None:
                    error_message = f"No pawn with this ID: {attacker_display}"
                    continue

                enemy_color = Tile.PURPLE
                target = board.get_pawn_by_display(target_display, enemy_color)
                if target is None:
                    error_message = f"No target pawn with this ID: {target_display}"
                    continue

                ni, nj = target.i, target.j
                moves = board.possible_moves(attacker.id)
                found = False
                for m in moves:
                    if m[0] == "attack" and m[1] == ni and m[2] == nj:
                        board.move_pawn(attacker.id, ni, nj)
                        found = True
                        break

                if not found:
                    error_message = f"The pawn {attacker_display} cannot attack the pawn {target_display}"
                    continue

            error_message = None
            turn = Tile.PURPLE

        # AI turn
        elif turn == Tile.PURPLE:
            time.sleep(0.8)
            _, best_move = minimax(board, Tile.PURPLE, depth)
            if best_move:
                pid, action_type, ni, nj = best_move
                board.move_pawn(pid, ni, nj)

            turn = Tile.WHITE

if __name__ == "__main__":
    main()
