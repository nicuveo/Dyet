# image.py
#
# This class defines a basic 2D image with PPM export support.



##########################################
# Imports

import tools.math_utils as math_utils



##########################################
# Classes

class Image:
    '''A 2D image of immutable dimensions'''

    # constructor

    def __init__(self, width, height, pixel = (255, 255, 255)):
        self._width = width
        self._height = height
        self._data = [pixel] * width * height


    # operators

    def __len__(self):
        return len(self._data)
    def __iter__(self):
        return self._data.__iter__()
    def __getitem__(self, key):
        return self.pixel(*key)
    def __setitem__(self, key, value):
        return self.pixel_set(*key, p = value)


    # accessors

    @staticmethod
    def clamp_int(p):
        return math_utils.clamp(p, 0, 255)
    @staticmethod
    def clamp_pixel(p):
        return (Image.clamp_int(p[0]), Image.clamp_int(p[1]), Image.clamp_int(p[2]))

    @property
    def width(self): return self._width
    @property
    def height(self): return self._height

    def pixel(self, x, y):
        return self._data[y * self.width + x]


    # mutators

    def pixel_set(self, x, y, p):
        self._data[y * self.width + x] = Image.clamp_pixel(p)

    def transform(self, fun):
        self._data = [fun(x) for x in self._data]


    # translators

    def to_ppm_string(self):
        return str.format("P3\n{width} {height}\n255\n{data}",
                          width  = self.width,
                          height = self.height,
                          data   = "\n".join([str.format("{0:3} {1:3} {2:3}", r, g, b) for (r, g, b) in self._data]))



##########################################
# Unit tests

if __name__ == "__main__":
    import unittest

    class ImageTest(unittest.TestCase):
        def test_clamp_int(self):
            self.assertEqual(  0, Image.clamp_int(-100))
            self.assertEqual(  0, Image.clamp_int(   0))
            self.assertEqual( 42, Image.clamp_int(  42))
            self.assertEqual(255, Image.clamp_int( 255))
            self.assertEqual(255, Image.clamp_int( 666))

        def test_clamp_pixel(self):
            self.assertEqual((  0,   0,  42), Image.clamp_pixel((-100,    0,   42)));
            self.assertEqual((  0,  42, 255), Image.clamp_pixel((   0,   42,  255)));
            self.assertEqual(( 42, 255,   0), Image.clamp_pixel((  42,  666, -100)));
            self.assertEqual((255,   0,   0), Image.clamp_pixel(( 666, -100,    0)));

        def test_width_height(self):
            i = Image(42, 69)
            self.assertEqual(i.width,  42)
            self.assertEqual(i.height, 69)

        def test_ppm(self):
            self.assertEqual("P3\n2 2\n255\n100 150 200\n100 150 200\n100 150 200\n100 150 200",
                             Image(2, 2, (100, 150, 200)).to_ppm_string())

    unittest.main(verbosity = 0)
