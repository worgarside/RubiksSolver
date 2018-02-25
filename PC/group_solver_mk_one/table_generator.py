import pickle

from cube.cube_class import Cube, SOLVED_POS
from cube.move_class import Move
from cube.moves import dyn_move
from cube.position_class import Position  # (pos_id, position, depth, move_sequence)

MOVE_GROUP = [Move.U2, Move.D2, Move.L2, Move.R2, Move.F2, Move.B2]

OPPOSITE_MOVE_DICT = {
    Move.U2: Move.D2,
    Move.D2: Move.U2,
    Move.L2: Move.R2,
    Move.R2: Move.L2,
    Move.F2: Move.B2,
    Move.B2: Move.F2,
}


def generate_table(db):
    position_dict = {}
    position_set = set()
    depth = 0
    position_dict[depth] = {Position(depth, SOLVED_POS, [Move.NONE])}
    tree_width = 1

    while tree_width > 0:
        position_dict[depth + 1] = []
        tree_width = 0
        depth += 1
        print(depth)

        for p in position_dict[depth - 1]:
            for m in MOVE_GROUP:

                # Prevent undoing moves
                if p.move_sequence[-1] == m or \
                        (p.move_sequence[-1] == OPPOSITE_MOVE_DICT[m] and p.move_sequence[-2] == m):
                    continue

                c = Cube(p.position, True)
                dyn_move(c, m)

                if c.position not in position_set:
                    position_dict[depth].append(Position(depth, c.position, p.move_sequence + [m]))
                    position_set.add(c.position)
                    tree_width += 1

    for depth, positions in position_dict.items():
        for position in positions:
            db.query('INSERT INTO g_solve_mk1_p4 VALUES (?, ?, ?)',
                     (position.depth, position.position, pickle.dumps(position.move_sequence[1:])))
    db.commit()