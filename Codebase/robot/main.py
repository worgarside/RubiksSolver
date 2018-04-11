import os
import pickle
import socket
from time import sleep, time

from ev3dev.ev3 import Sound
from ev3dev.helper import MotorStall

from robot.robot_class import Robot

IP_DICT = {
    'WILLS-SURFACE @ ONEPLUS 3': '192.168.43.188',
    'WILLS-DESKTOP @ HOME': '192.168.0.21',
    'WILLS-SURFACE @ EDGE LANE': '192.168.1.84'
}

CURRENT_IP = IP_DICT['WILLS-DESKTOP @ HOME']


def create_socket():
    conn = socket.socket()

    print('Connecting to %s:%s...' % (CURRENT_IP, 3000), end='')
    conn.connect((CURRENT_IP, 3000))
    print('!')
    Sound.speak('connected to server')
    sleep(1.5)
    return conn


def create_robot():
    robot = Robot()
    return robot


def scan_cube(robot):
    start_time = time()
    pos = robot.scan_cube()
    end_time = time()

    file_path = '%s/scan_times.csv' % os.path.abspath(os.path.dirname(__file__))
    with open(file_path) as csv_read:
        (avg_time_str, scan_count_str) = csv_read.readline().split(',')

    old_avg_time = float(avg_time_str)
    old_scan_count = int(scan_count_str)

    new_scan_time = end_time - start_time
    new_scan_count = old_scan_count + 1
    new_avg_time = ((old_avg_time * old_scan_count) + new_scan_time) / new_scan_count

    with open(file_path, 'wb') as csv_write:
        csv_write.write(bytes('%0.3f,%i' % (new_avg_time, new_scan_count), 'UTF-8'))

    if new_scan_time > new_avg_time:
        print('Scan time of %0.1fs was ~%0.1fs slower than average' % (new_scan_time, new_scan_time - new_avg_time))
    else:
        print('Scan time of %0.1fs was ~%0.1fs faster than average' % (new_scan_time, new_avg_time - new_scan_time))

    return pos


def main():
    conn = create_socket()
    robot = create_robot()

    try:
        pos = scan_cube(robot)
        pos_str = ''.join(pos)
        conn.send(pos_str.encode())

        sequence = ''
        sequence_received = False
        while not sequence_received:
            data = conn.recv(1024)
            sequence = pickle.loads(data)
            if sequence != '':
                sequence_received = True

        print(sequence)

        robot.run_move_sequence(sequence)
    except MotorStall as err:
        print('\n\n %s' % err)

    robot.exit()


if __name__ == '__main__':
    main()