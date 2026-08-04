def read_first_line(path):
    with open(path, "r") as f:
        line = f.readline()
    return line