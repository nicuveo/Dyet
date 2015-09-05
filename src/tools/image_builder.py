# image_builder.py
#
# This class provides image building functions



##########################################
# Imports

from image import Image



##########################################
# Declarations

SAME_DIRECTION = 0
PLUS_90        = 1
PLUS_180       = 2
MINUS_90       = 3



def paste_sub_image(image, sub_image, rx, ry, direction = 0):
    assert(direction in range(0, 4))
    w = sub_image.width()
    h = sub_image.height()
    pfun = {
        0: lambda x, y: (rx + x,         ry + y),
        1: lambda x, y: (rx + h - 1 - y, ry + x),
        2: lambda x, y: (rx + w - 1 - x, ry + h - 1 - y),
        3: lambda x, y: (rx + y,         ry + w - 1 - x)
        }[direction]

    for y in range(0, h):
        for x in range(0, w):
            pos = pfun(x, y)
            image.pixel_set(pos[0], pos[1], sub_image.pixel(x, y))


def draw_rect(image, p0, p1, color):
    for row in range(p0[1], p1[1] + 1):
        for col in range(p0[0], p1[0] + 1):
            image.pixel_set(col, row, color)



##########################################
# Unit tests

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity = 0)
