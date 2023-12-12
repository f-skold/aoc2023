def read_file_contents(filename):
    temp = None
    with open(f"../testdata/{filename}", "rt") as fp:
        temp = fp.readlines()
    return temp
