import pickle
import socket
import time
from _tkinter import TclError
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from queue import LifoQueue

import colorama

from cube.cube_class import Cube, SOLVED_POS
from cube.moves import *
from data.database_manager import DatabaseManager
from group_solver.good_bad_edges import make_all_edges_good
from group_solver.good_bad_corners import make_all_corners_good
from gui.interface import Interface
from robot.move_converter import convert_sequence
from tree_solver.tree_generator import generate_tree

GROUP_THREE = [MOVE.U2, MOVE.D2, MOVE.L2, MOVE.R2, MOVE.F2, MOVE.B2]
GROUP_TWO = [MOVE.U2, MOVE.D2, MOVE.L, MOVE.R, MOVE.F2, MOVE.B2]
GROUP_ONE = [MOVE.U2, MOVE.D2, MOVE.L, MOVE.R, MOVE.F, MOVE.B]
GROUP_ZERO = [MOVE.U, MOVE.D, MOVE.L, MOVE.R, MOVE.F, MOVE.B]

GROUP_COMPLETE = [MOVE.U, MOVE.NOT_U, MOVE.U2, MOVE.D, MOVE.NOT_D, MOVE.D2,
                  MOVE.L, MOVE.NOT_L, MOVE.L2, MOVE.R, MOVE.NOT_R, MOVE.R2,
                  MOVE.F, MOVE.NOT_F, MOVE.F2, MOVE.B, MOVE.NOT_B, MOVE.B2]

GROUP_QUARTERS = [MOVE.U, MOVE.NOT_U, MOVE.D, MOVE.NOT_D,
                  MOVE.L, MOVE.NOT_L, MOVE.R, MOVE.NOT_R,
                  MOVE.F, MOVE.NOT_F, MOVE.B, MOVE.NOT_B, ]


def init_db():
    db = DatabaseManager('PC/data/db.sqlite')

    db.query('DROP TABLE IF EXISTS positions')
    db.query('''CREATE TABLE IF NOT EXISTS positions (
                    id INTEGER PRIMARY KEY,
                    position TEXT NOT NULL,
                    depth INTEGER NOT NULL,
                    move_chain TEXT NOT NULL)
                ''')

    return db


def group_solve(cube=Cube(SOLVED_POS)):
    sequence_list = []
    
    good_edge_pos = make_all_edges_good(cube.position_reduced)
    good_edge_sequence = good_edge_pos.move_sequence[1:]
    sequence_list.append(good_edge_sequence)
    
    good_edge_cube = deepcopy(cube)
    for move in good_edge_sequence:
        dyn_move(good_edge_cube, move)

    print(good_edge_cube)

    good_corner_pos = make_all_corners_good(good_edge_cube.position_reduced)
    good_corner_sequence = good_corner_pos.move_sequence[1:]
    sequence_list.append(good_corner_sequence)

    good_corner_cube = deepcopy(good_edge_cube)
    for move in good_corner_sequence:
        dyn_move(good_corner_cube, move)

    print(good_corner_cube)

    total_sequence = []
    for sequence in sequence_list:
        print(sequence)
        total_sequence.extend(sequence)

    return total_sequence


def tree_solve():
    BaseManager.register('LifoQueue', LifoQueue)
    manager = BaseManager()
    manager.start()
    position_queue = manager.LifoQueue()

    process_list = []

    cube = Cube()
    u(cube)
    not_r(cube)
    not_b(cube)

    tree_process = Process(target=time_function, args=(generate_tree, cube, GROUP_COMPLETE, position_queue,),
                           name='tree_process')
    process_list.append(tree_process)

    for p in process_list:
        p.start()

    try:
        window = Interface(position_queue)
        window.root.after(0, window.update_cube_net)
        window.root.mainloop()
    except TclError as err:
        print(err)

    for p in process_list:
        print('Terminating %s' % p.name)
        p.terminate()  # kill process when window is closed


def time_function(func, *args):
    start = int(round(time.time() * 1000))
    result = func(*args)
    end = int(round(time.time() * 1000))
    total = (end - start) / 1000
    print('Time: %0.2fs' % total)
    return result


def create_socket():
    conn = socket.socket()
    conn.bind(('0.0.0.0', 3000))
    print('Listening for connection...')
    conn.listen(1)
    c, client_address = conn.accept()
    print('EV3 connected @ %s:%s\n' % (client_address[0], client_address[1]))
    return c


def get_current_position(conn):
    pos_received = False
    position = ''
    while not pos_received:
        position = conn.recv(1024).decode()
        if position != '':
            pos_received = True
    return position


def main():
    conn = create_socket()
    position = get_current_position(conn)

    # position = 'OBROWROGRWWWBRBWWWGOGWOYGGGWRYBBBYYYBOBYYYGRGOGROYROBR'
    # position = 'WBWWWWWGWOOOGWGRRRBWBBOGOGRGRBRBOOOOGYGRRRBYBYGYYYYYBY'
    # position = 'YWRBWYOOWOOBYYOGBYBRGGOGWGWBRYGBOWRRGWBRRYGRBWOWYYBOGR'

    print('Scanned position: %s' % position)

    cube = Cube(position)
    solve_sequence = []

    print(cube)

    solve_sequence.extend(time_function(group_solve, cube))

    robot_sequence = convert_sequence(cube, solve_sequence)
    print(robot_sequence)

    conn.send(pickle.dumps(robot_sequence))
    conn.close()


if __name__ == '__main__':
    colorama.init()
    main()
