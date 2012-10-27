# parser.py



########## Declarations ##########

def parse(data):
    lines = data.replace(";", "\n").strip("\n").split("\n")
    for line_argv in [line.strip().split(" ") for line in lines]:
        yield line_argv
