import colorama
from .rotation_class import Rotation
from .side_class import Side

colorama.init()

SOLVED_POS = 'WWWWWWWWWOOOGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBYYYYYYYYY'

class Cube:

    def __init__(self, position = SOLVED_POS):
        self.position = position
        self.color_position = ""
        self._color_dict = {'R': '\033[31m', 'B': '\033[34m', 'G': '\033[32m', 'O': '\033[35m', 'W': '\033[37m', 'Y': '\033[33m'}
        self.update_sides()

    def __str__(self):
        """Returns a colored net of the Cube"""
        linebreak_dict = {2: "\n      ", 5: "\n      ", 8: "\n", 20: "\n", 32: "\n", 44: "\n      ", 47: "\n      ", 50: "\n      "}
        char_net = "      "
        for index, color in enumerate(self.position):
            char_net += self._color_dict[color] + color + '\033[0m' + linebreak_dict.get(index, " ")
        char_net += "\n"
        return char_net

    # Updates the sides of the cube from the main position variable
    def update_sides(self):
        self.up = self.position[:9]
        self.down = self.position[45:54]
        self.left = self.position[9:12] + self.position[21:24] + self.position[33:36]
        self.right = self.position[15:18] + self.position[27:30] + self.position[39:42]
        self.front = self.position[12:15] + self.position[24:27] + self.position[36:39]
        self.back = self.position[18:21] + self.position[30:33] + self.position[42:45]
        self.update_pos_colors()

    def update_pos_colors(self):
        for color in self.position:
            self.color_position += self._color_dict[color] + color + '\033[0m'

    # Setter methods
    def set_up(self, pos):
        if len(pos) == 9:
            self.position = pos + self.position[9:]
            self.update_sides()
        else:
            print('\nset_up: len(position) != 9')
            exit()

    def set_down(self, pos):
        if len(pos) == 9:
            self.position = self.position[:45] + pos
            self.update_sides()
        else:
            print('\nset_down: len(position) != 9')
            exit()

    def set_left(self, pos):
        if len(pos) == 9:
            self.position = self.position[:9] + pos[:3] + self.position[12:21] + pos[3:6] + self.position[24:33] + pos[6:] + \
                            self.position[36:]
            self.update_sides()
        else:
            print('\nset_left: len(position) != 9')
            exit()

    def set_right(self, pos):
        if len(pos) == 9:
            self.position = self.position[:15] + pos[:3] + self.position[18:27] + pos[3:6] + self.position[30:39] + pos[6:] + \
                            self.position[42:]
            self.update_sides()
        else:
            print('\nset_right: len(position) != 9')
            exit()

    def set_front(self, pos):
        if len(pos) == 9:
            self.position = self.position[:12] + pos[:3] + self.position[15:24] + pos[3:6] + self.position[27:36] + pos[6:] + \
                            self.position[39:]
            self.update_sides()
        else:
            print('\nset_front: len(position) != 9')
            exit()

    def set_back(self, pos):
        if len(pos) == 9:
            self.position = self.position[:18] + pos[:3] + self.position[21:30] + pos[3:6] + self.position[33:42] + pos[6:] + \
                            self.position[45:]
            self.update_sides()
        else:
            print('\nset_back: len(position) != 9')
            exit()

    def rotate_side(self, direction, side):
        c = Cube(self.position)

        if direction == Rotation.CLOCKWISE:
            if side == Side.LEFT:
                self.set_left(c.left[6:7] + c.left[3:4] + c.left[0:1] + c.left[7:8] + c.left[4:5]
                              + c.left[1:2] + c.left[8:9] + c.left[5:6] + c.left[2:3])
            elif side == Side.RIGHT:
                self.set_right(c.right[6:7] + c.right[3:4] + c.right[0:1] + c.right[7:8] + c.right[4:5]
                               + c.right[1:2] + c.right[8:9] + c.right[5:6] + c.right[2:3])
            elif side == Side.FRONT:
                self.set_front(c.front[6:7] + c.front[3:4] + c.front[0:1] + c.front[7:8] + c.front[4:5]
                               + c.front[1:2] + c.front[8:9] + c.front[5:6] + c.front[2:3])
            elif side == Side.BACK:
                self.set_back(c.back[6:7] + c.back[3:4] + c.back[0:1] + c.back[7:8] + c.back[4:5]
                              + c.back[1:2] + c.back[8:9] + c.back[5:6] + c.back[2:3])
            elif side == Side.UP:
                self.set_up(c.up[6:7] + c.up[3:4] + c.up[0:1] + c.up[7:8] + c.up[4:5]
                            + c.up[1:2] + c.up[8:9] + c.up[5:6] + c.up[2:3])
            elif side == Side.DOWN:
                self.set_down(c.down[6:7] + c.down[3:4] + c.down[0:1] + c.down[7:8] + c.down[4:5]
                              + c.down[1:2] + c.down[8:9] + c.down[5:6] + c.down[2:3])
            else:
                print('\nrotate_side_cw: invalid side')
                exit()
        elif direction == Rotation.COUNTER_CLOCKWISE:

            if side == Side.LEFT:
                self.set_left(c.left[2:3] + c.left[5:6] + c.left[8:9] + c.left[1:2] + c.left[4:5]
                              + c.left[7:8] + c.left[0:1] + c.left[3:4] + c.left[6:7])
            elif side == Side.RIGHT:
                self.set_right(c.right[2:3] + c.right[5:6] + c.right[8:9] + c.right[1:2] + c.right[4:5]
                               + c.right[7:8] + c.right[0:1] + c.right[3:4] + c.right[6:7])
            elif side == Side.FRONT:
                self.set_front(c.front[2:3] + c.front[5:6] + c.front[8:9] + c.front[1:2] + c.front[4:5]
                               + c.front[7:8] + c.front[0:1] + c.front[3:4] + c.front[6:7])
            elif side == Side.BACK:
                self.set_back(c.back[2:3] + c.back[5:6] + c.back[8:9] + c.back[1:2] + c.back[4:5]
                              + c.back[7:8] + c.back[0:1] + c.back[3:4] + c.back[6:7])
            elif side == Side.UP:
                self.set_up(c.up[2:3] + c.up[5:6] + c.up[8:9] + c.up[1:2] + c.up[4:5]
                            + c.up[7:8] + c.up[0:1] + c.up[3:4] + c.up[6:7])
            elif side == Side.DOWN:
                self.set_down(c.down[2:3] + c.down[5:6] + c.down[8:9] + c.down[1:2] + c.down[4:5]
                              + c.down[7:8] + c.down[0:1] + c.down[3:4] + c.down[6:7])
            else:
                print('\nrotate_side_ccw: invalid side')
                exit()
        else:
            print('\nrotate_side: invalid direction')
            exit()