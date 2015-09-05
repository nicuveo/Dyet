# parser.py



##########################################
# Declarations

def parse(data):
    lines = data.replace(";", "\n").strip("\n").split("\n")
    for line_argv in [line.strip().split(" ") for line in lines if line]:
        yield line_argv



##########################################
# Unit tests

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity = 0)
