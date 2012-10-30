# command.py
#
# This file sets up an enumeration of all possible commands.



########## Declarations ##########

class Command:
    def __init__(self, name, hue_delta, lightness_delta):
        self.__name = name
        self.__hue_delta = hue_delta
        self.__lightness_delta = lightness_delta

    def name(self):            return self.__name
    def hue_delta(self):       return self.__hue_delta
    def lightness_delta(self): return self.__lightness_delta


class Commands:
    NOOP      = Command("noop",      0, 0)
    PUSH      = Command("push",      0, 1)
    POP       = Command("pop",       0, 2)
    ADD       = Command("add",       1, 0)
    SUBSTRACT = Command("substract", 1, 1)
    MULTIPLY  = Command("multiply",  1, 2)
    DIVIDE    = Command("divide",    2, 0)
    MOD       = Command("mod",       2, 1)
    NOT       = Command("not",       2, 2)
    GREATER   = Command("greater",   3, 0)
    POINTER   = Command("pointer",   3, 1)
    SWITCH    = Command("switch",    3, 2)
    DUPLICATE = Command("duplicate", 4, 0)
    ROLL      = Command("roll",      4, 1)
    IN_INT    = Command("in_int",    4, 2)
    IN_CHAR   = Command("in_char",   5, 0)
    OUT_INT   = Command("out_int",   5, 1)
    OUT_CHAR  = Command("out_char",  5, 2)

    list = []
    map = {}



########## Static init ##########

for cmd in [Commands.NOOP,
            Commands.PUSH,
            Commands.POP,
            Commands.ADD,
            Commands.SUBSTRACT,
            Commands.MULTIPLY,
            Commands.DIVIDE,
            Commands.MOD,
            Commands.NOT,
            Commands.GREATER,
            Commands.POINTER,
            Commands.SWITCH,
            Commands.DUPLICATE,
            Commands.ROLL,
            Commands.IN_INT,
            Commands.IN_CHAR,
            Commands.OUT_INT,
            Commands.OUT_CHAR]:
    Commands.list.append(cmd)
    Commands.map[cmd.name()] = cmd



########## Unit tests ##########

if __name__ == "__main__":
    import unittest

    class CommandsTest(unittest.TestCase):
        def test_size(self):
            ref = [x for x in dir(Commands) if not x.startswith("__")]
            self.assertEqual(len(ref) - 2, len(Commands.list))
            self.assertEqual(len(ref) - 2, len(Commands.map))

    unittest.main(verbosity = 0)
