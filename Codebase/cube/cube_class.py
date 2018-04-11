from enum import Enum, unique

SOLVED_POS = 'WWWWWWWWWOOOGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBYYYYYYYYY'


class Cube:
    def __init__(self, position=SOLVED_POS, temporary=False):
        self.position = position
        self.position_reduced = ''
        self.color_position = ''
        self.temporary = temporary

        self.up = ''
        self.down = ''
        self.left = ''
        self.right = ''
        self.front = ''
        self.back = ''

        self.robot_solve_sequence = []

        self.reduction_dict = {Color.ORANGE: Color.RED, Color.YELLOW: Color.WHITE, Color.GREEN: Color.BLUE,
                               Color.RED: Color.RED, Color.WHITE: Color.WHITE, Color.BLUE: Color.BLUE}
        self.opposite_faces_dict = {Face.UP: Face.DOWN, Face.DOWN: Face.UP, Face.LEFT: Face.RIGHT,
                                    Face.RIGHT: Face.LEFT, Face.FRONT: Face.BACK, Face.BACK: Face.FRONT}
        self.facelet_face_dict = {0: Face.UP, 1: Face.UP, 2: Face.UP, 3: Face.UP, 4: Face.UP, 5: Face.UP, 6: Face.UP,
                                  7: Face.UP, 8: Face.UP, 9: Face.LEFT, 10: Face.LEFT, 11: Face.LEFT, 12: Face.FRONT,
                                  13: Face.FRONT, 14: Face.FRONT, 15: Face.RIGHT, 16: Face.RIGHT, 17: Face.RIGHT,
                                  18: Face.BACK, 19: Face.BACK, 20: Face.BACK, 21: Face.LEFT, 22: Face.LEFT,
                                  23: Face.LEFT, 24: Face.FRONT, 25: Face.FRONT, 26: Face.FRONT, 27: Face.RIGHT,
                                  28: Face.RIGHT, 29: Face.RIGHT, 30: Face.BACK, 31: Face.BACK, 32: Face.BACK,
                                  33: Face.LEFT, 34: Face.LEFT, 35: Face.LEFT, 36: Face.FRONT, 37: Face.FRONT,
                                  38: Face.FRONT, 39: Face.RIGHT, 40: Face.RIGHT, 41: Face.RIGHT, 42: Face.BACK,
                                  43: Face.BACK, 44: Face.BACK, 45: Face.DOWN, 46: Face.DOWN, 47: Face.DOWN,
                                  48: Face.DOWN, 49: Face.DOWN, 50: Face.DOWN, 51: Face.DOWN, 52: Face.DOWN,
                                  53: Face.DOWN}
        self._color_print_dict = {Color.RED: '\033[31m', Color.BLUE: '\033[34m', Color.GREEN: '\033[32m',
                                  Color.ORANGE: '\033[35m', Color.WHITE: '\033[37m', Color.YELLOW: '\033[33m',
                                  Color.DARK: '\033[30m', Color.NONE: '\033[36m'}

        self.update_fields()

    def __str__(self):
        """ Returns a colored net of the Cube """
        linebreak_dict = {2: '\n      ', 5: '\n      ', 8: '\n', 20: '\n', 32: '\n', 44: '\n      ', 47: '\n      ',
                          50: '\n      '}
        char_net = '\n      '
        for index, color in enumerate(self.position):
            char_net += self._color_print_dict[Color(color)] + color + '\033[0m' + linebreak_dict.get(index, ' ')
        char_net += '\n'
        return char_net

    # ------------------ Update Methods ------------------ #

    def update_fields(self):
        """Updates all fields of Cube from position"""
        self.update_faces()
        if not self.temporary:
            self.update_reduced_cube()
            self.update_pos_colors()

    def update_faces(self):
        """ Updates the faces of the cube from the main position variable """
        self.up = self.position[:9]
        self.down = self.position[45:54]
        self.left = self.position[9:12] + self.position[21:24] + self.position[33:36]
        self.right = self.position[15:18] + self.position[27:30] + self.position[39:42]
        self.front = self.position[12:15] + self.position[24:27] + self.position[36:39]
        self.back = self.position[18:21] + self.position[30:33] + self.position[42:45]

    def update_pos_colors(self):
        """Updates position field with colored output"""
        self.color_position = ''
        for color in self.position:
            self.color_position += self._color_print_dict[Color(color)] + color + '\033[0m'

    def update_reduced_cube(self):
        self.position_reduced = ''
        for color in self.position:
            self.position_reduced += self.reduction_dict.get(Color(color), Color(color)).value

    # ------------------ Setter Methods ------------------ #
    """Each of these sets the relevant face facelets to the given string and updates the relevant fields"""

    def set_up(self, pos):
        if len(pos) == 9:
            self.position = pos + self.position[9:]
            self.update_fields()
        else:
            print('\nset_up: len(position) != 9')
            exit()

    def set_down(self, pos):
        if len(pos) == 9:
            self.position = self.position[:45] + pos
            self.update_fields()
        else:
            print('\nset_down: len(position) != 9')
            exit()

    def set_left(self, pos):
        if len(pos) == 9:
            self.position = self.position[:9] + pos[:3] + self.position[12:21] + pos[3:6] + \
                            self.position[24:33] + pos[6:] + self.position[36:]
            self.update_fields()
        else:
            print('\nset_left: len(position) != 9')
            exit()

    def set_right(self, pos):
        if len(pos) == 9:
            self.position = self.position[:15] + pos[:3] + self.position[18:27] + pos[3:6] + \
                            self.position[30:39] + pos[6:] + self.position[42:]
            self.update_fields()
        else:
            print('\nset_right: len(position) != 9')
            exit()

    def set_front(self, pos):
        if len(pos) == 9:
            self.position = self.position[:12] + pos[:3] + self.position[15:24] + pos[3:6] + \
                            self.position[27:36] + pos[6:] + self.position[39:]
            self.update_fields()
        else:
            print('\nset_front: len(position) != 9')
            exit()

    def set_back(self, pos):
        if len(pos) == 9:
            self.position = self.position[:18] + pos[:3] + self.position[21:30] + pos[3:6] + \
                            self.position[33:42] + pos[6:] + self.position[45:]
            self.update_fields()
        else:
            print('\nset_back: len(position) != 9')
            exit()

    def rotate_face(self, direction, face):
        """Rotates the 9 facelets of a face"""
        c = Cube(self.position)

        if direction == Rotation.CLOCKWISE:
            if face == Face.LEFT:
                self.set_left(c.left[6:7] + c.left[3:4] + c.left[0:1] + c.left[7:8] + c.left[4:5]
                              + c.left[1:2] + c.left[8:9] + c.left[5:6] + c.left[2:3])
            elif face == Face.RIGHT:
                self.set_right(c.right[6:7] + c.right[3:4] + c.right[0:1] + c.right[7:8] + c.right[4:5]
                               + c.right[1:2] + c.right[8:9] + c.right[5:6] + c.right[2:3])
            elif face == Face.FRONT:
                self.set_front(c.front[6:7] + c.front[3:4] + c.front[0:1] + c.front[7:8] + c.front[4:5]
                               + c.front[1:2] + c.front[8:9] + c.front[5:6] + c.front[2:3])
            elif face == Face.BACK:
                self.set_back(c.back[6:7] + c.back[3:4] + c.back[0:1] + c.back[7:8] + c.back[4:5]
                              + c.back[1:2] + c.back[8:9] + c.back[5:6] + c.back[2:3])
            elif face == Face.UP:
                self.set_up(c.up[6:7] + c.up[3:4] + c.up[0:1] + c.up[7:8] + c.up[4:5]
                            + c.up[1:2] + c.up[8:9] + c.up[5:6] + c.up[2:3])
            elif face == Face.DOWN:
                self.set_down(c.down[6:7] + c.down[3:4] + c.down[0:1] + c.down[7:8] + c.down[4:5]
                              + c.down[1:2] + c.down[8:9] + c.down[5:6] + c.down[2:3])
            else:
                print('\nrotate_face_cw: invalid face')
                exit()
        elif direction == Rotation.COUNTER_CLOCKWISE:

            if face == Face.LEFT:
                self.set_left(c.left[2:3] + c.left[5:6] + c.left[8:9] + c.left[1:2] + c.left[4:5]
                              + c.left[7:8] + c.left[0:1] + c.left[3:4] + c.left[6:7])
            elif face == Face.RIGHT:
                self.set_right(c.right[2:3] + c.right[5:6] + c.right[8:9] + c.right[1:2] + c.right[4:5]
                               + c.right[7:8] + c.right[0:1] + c.right[3:4] + c.right[6:7])
            elif face == Face.FRONT:
                self.set_front(c.front[2:3] + c.front[5:6] + c.front[8:9] + c.front[1:2] + c.front[4:5]
                               + c.front[7:8] + c.front[0:1] + c.front[3:4] + c.front[6:7])
            elif face == Face.BACK:
                self.set_back(c.back[2:3] + c.back[5:6] + c.back[8:9] + c.back[1:2] + c.back[4:5]
                              + c.back[7:8] + c.back[0:1] + c.back[3:4] + c.back[6:7])
            elif face == Face.UP:
                self.set_up(c.up[2:3] + c.up[5:6] + c.up[8:9] + c.up[1:2] + c.up[4:5]
                            + c.up[7:8] + c.up[0:1] + c.up[3:4] + c.up[6:7])
            elif face == Face.DOWN:
                self.set_down(c.down[2:3] + c.down[5:6] + c.down[8:9] + c.down[1:2] + c.down[4:5]
                              + c.down[7:8] + c.down[0:1] + c.down[3:4] + c.down[6:7])
            else:
                print('\nrotate_face_ccw: invalid face')
                exit()
        else:
            print('\nrotate_face: invalid direction')
            exit()

    # ------------------ Getter Methods ------------------ #

    def get_color_of_face(self, **kwargs):
        if 'facelet' in kwargs:
            facelet = kwargs['facelet']
            try:
                face = self.facelet_face_dict[facelet]
                return Color(eval('self.%s' % face.name.lower())[4])
            except KeyError:
                print('Invalid Facelet number passed to method')

        if 'face' in kwargs:
            face = kwargs['face']
            try:
                return Color(eval('self.%s' % face.name.lower())[4])
            except AttributeError:
                print('Invalid Face passed to method')

    def get_face_with_color(self, **kwargs):
        if 'color' in kwargs:
            color = kwargs['color']
            faces = {Face.UP: self.up, Face.DOWN: self.down,
                     Face.LEFT: self.left, Face.RIGHT: self.right,
                     Face.FRONT: self.front, Face.BACK: self.back}

            for face, colors in faces.items():
                if Color(colors[4]) == color:
                    return face
            print("No faces found with color '%s'" % str(color))
            raise AttributeError


@unique
class Color(Enum):
    """An Enum Class to hold potential colors scanned by the LEGO Color Sensor"""

    NONE = 'N'
    DARK = 'D'  # DARK (not 'BLACK') to show up with any color reading errors (differentiates it from BLUE)
    BLUE = 'B'
    GREEN = 'G'
    YELLOW = 'Y'
    RED = 'R'
    WHITE = 'W'
    ORANGE = 'O'  # Color Sensor actually reads BROWN but ORANGE is used to avoid confusion


@unique
class Move(Enum):
    NONE = '-'
    U = 'U '
    NOT_U = "U'"
    U2 = 'U2'
    D = 'D '
    NOT_D = "D'"
    D2 = 'D2'
    L = 'L '
    NOT_L = "L'"
    L2 = 'L2'
    R = 'R '
    NOT_R = "R'"
    R2 = 'R2'
    F = 'F '
    NOT_F = "F'"
    F2 = 'F2'
    B = 'B '
    NOT_B = "B'"
    B2 = 'B2'
    M = 'M '
    NOT_M = "M'"
    M2 = 'M2'
    E = 'E '
    NOT_E = "E'"
    E2 = 'E2'
    S = 'S '
    NOT_S = "S'"
    S2 = 'S2'
    X = 'X '
    NOT_X = "X'"
    X2 = 'X2'
    Y = 'Y '
    NOT_Y = "Y'"
    Y2 = 'Y2'
    Z = 'Z '
    NOT_Z = "Z'"
    Z2 = 'Z2'


@unique
class Face(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    FRONT = 'F'
    BACK = 'B'


@unique
class Rotation(Enum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1


class Position:
    def __init__(self, depth, position, move_sequence, pos_id=0):
        self.depth = depth
        self.position = position
        self.move_sequence = move_sequence
        self.pos_id = pos_id

    def __str__(self):
        return self.position + ' ' + str(self.move_sequence)