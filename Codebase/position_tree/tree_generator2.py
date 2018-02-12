from cube.cube_class import Cube, SOLVED_POS
from position_tree.position_class import Position  # (id, position, depth, parent_id, parent_move, move_chain)
from cube.move_class import Move as MOVE
from cube.moves import dyn_move


def generate_tree(cube, move_group, queue):
    solved = False
    positions = {}
    depth = 0
    pos_id = 0
    position_set = set()
    positions[depth] = {Position(0, cube.position, depth, -1, MOVE.NONE, [])}
    solution_move_chain = []

    while not solved:
        positions[depth + 1] = []
        for p in positions[depth]:
            for m in move_group:
                c = Cube(p.position)
                dyn_move(c, m)
                pos_id += 1
                positions[depth + 1].append(
                    Position(pos_id, c.position, depth + 1, p.id, str(m), p.move_chain + [str(m)[5:]]))

                if c.position not in position_set:

                    queue.put(c.position)

                    pos_id += 1
                    positions[depth + 1].append(
                        Position(pos_id, c.position, depth + 1, p.id, str(m),
                                 p.move_chain + [str(m)[5:]]))
                    position_set.add(c.position)

                    if c.position == SOLVED_POS:
                        solved = True
                        solution_move_chain = p.move_chain + [str(m)[5:]]
                        break
            if solved:
                break
        depth += 1
    print("\nSOLVED: %s" % str(solution_move_chain))