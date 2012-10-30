# color.py
#
# This file sets up an enumeration of useful colors



########## Declarations ##########

class Color:
    def __init__(self, hue, lightness, rgb):
        self.__hue = hue
        self.__lightness = lightness
        self.__rgb = rgb

    def hue(self):       return self.__hue
    def lightness(self): return self.__lightness
    def rgb(self):       return self.__rgb


class Colors:
    RGB_R0 = (0xFF, 0xC0, 0xC0)
    RGB_R1 = (0xFF,    0,    0)
    RGB_R2 = (0xC0,    0,    0)
    RGB_Y0 = (0xFF, 0xFF, 0xC0)
    RGB_Y1 = (0xFF, 0xFF,    0)
    RGB_Y2 = (0xC0, 0xC0,    0)
    RGB_G0 = (0xC0, 0xFF, 0xC0)
    RGB_G1 = (   0, 0xFF,    0)
    RGB_G2 = (   0, 0xC0,    0)
    RGB_C0 = (0xC0, 0xFF, 0xFF)
    RGB_C1 = (   0, 0xFF, 0xFF)
    RGB_C2 = (   0, 0xC0, 0xC0)
    RGB_B0 = (0xC0, 0xC0, 0xFF)
    RGB_B1 = (   0,    0, 0xFF)
    RGB_B2 = (   0,    0, 0xC0)
    RGB_M0 = (0xFF, 0xC0, 0xFF)
    RGB_M1 = (0xFF,    0, 0xFF)
    RGB_M2 = (0xC0,    0, 0xC0)
    RGB_B  = (   0,    0,    0)
    RGB_W  = (0xFF, 0xFF, 0xFF)

    R0 = Color(0, 0, RGB_R0)
    R1 = Color(0, 1, RGB_R1)
    R2 = Color(0, 2, RGB_R2)
    Y0 = Color(1, 0, RGB_Y0)
    Y1 = Color(1, 1, RGB_Y1)
    Y2 = Color(1, 2, RGB_Y2)
    G0 = Color(2, 0, RGB_G0)
    G1 = Color(2, 1, RGB_G1)
    G2 = Color(2, 2, RGB_G2)
    C0 = Color(3, 0, RGB_C0)
    C1 = Color(3, 1, RGB_C1)
    C2 = Color(3, 2, RGB_C2)
    B0 = Color(4, 0, RGB_B0)
    B1 = Color(4, 1, RGB_B1)
    B2 = Color(4, 2, RGB_B2)
    M0 = Color(5, 0, RGB_M0)
    M1 = Color(5, 1, RGB_M1)
    M2 = Color(5, 2, RGB_M2)

    list = []
    map = {}


def next(color, hue_delta, lightness_delta):
    hue = (color.hue() + hue_delta) % 6
    lightness = (color.lightness() + lightness_delta) % 3
    return Colors.map[(hue, lightness)]

def prev(color, hue_delta, lightness_delta):
    return next(color, -hue_delta, -lightness_delta)

def command_next(color, command):
    return next(color, command.hue_delta(), command.lightness_delta())

def command_prev(color, command):
    return prev(color, command.hue_delta(), command.lightness_delta())

def command_list_next(color, commands):
    for command in commands:
        color = command_next(color, command)
    return color

def command_list_prev(color, commands):
    for command in commands:
        color = command_prev(color, command)
    return color



########## Static init ##########

for color in [Colors.R0, Colors.R1, Colors.R2,
              Colors.Y0, Colors.Y1, Colors.Y2,
              Colors.G0, Colors.G1, Colors.G2,
              Colors.C0, Colors.C1, Colors.C2,
              Colors.B0, Colors.B1, Colors.B2,
              Colors.M0, Colors.M1, Colors.M2]:
    Colors.list.append(color)
    Colors.map[(color.hue(), color.lightness())] = color



########## Unit tests ##########

if __name__ == "__main__":
    import unittest

    class ColorsTest(unittest.TestCase):
        def test_size(self):
            ref = [x for x in dir(Colors) if not x.startswith("__") and not x.startswith("RGB_")]
            self.assertEqual(len(ref) - 2, len(Colors.list))
            self.assertEqual(len(ref) - 2, len(Colors.map))

        def test_nexts(self):
            self.assertEqual(Colors.R0, next(Colors.R0, 0, 0))
            self.assertEqual(Colors.R1, next(Colors.R0, 0, 1))
            self.assertEqual(Colors.R2, next(Colors.R0, 0, 2))
            self.assertEqual(Colors.Y0, next(Colors.R0, 1, 0))
            self.assertEqual(Colors.Y1, next(Colors.R0, 1, 1))
            self.assertEqual(Colors.Y2, next(Colors.R0, 1, 2))
            self.assertEqual(Colors.G0, next(Colors.R0, 2, 0))
            self.assertEqual(Colors.G1, next(Colors.R0, 2, 1))
            self.assertEqual(Colors.G2, next(Colors.R0, 2, 2))
            self.assertEqual(Colors.C0, next(Colors.R0, 3, 0))
            self.assertEqual(Colors.C1, next(Colors.R0, 3, 1))
            self.assertEqual(Colors.C2, next(Colors.R0, 3, 2))
            self.assertEqual(Colors.B0, next(Colors.R0, 4, 0))
            self.assertEqual(Colors.B1, next(Colors.R0, 4, 1))
            self.assertEqual(Colors.B2, next(Colors.R0, 4, 2))
            self.assertEqual(Colors.M0, next(Colors.R0, 5, 0))
            self.assertEqual(Colors.M1, next(Colors.R0, 5, 1))
            self.assertEqual(Colors.M2, next(Colors.R0, 5, 2))

    unittest.main(verbosity = 0)
