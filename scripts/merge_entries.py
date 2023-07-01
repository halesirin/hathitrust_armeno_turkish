import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", dest="inputs", nargs="+", help="Input files")
    parser.add_argument("--output", dest="output", help="Output file")
    args, rest = parser.parse_known_args()
