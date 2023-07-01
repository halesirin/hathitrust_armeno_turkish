import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", dest="model", help="Input file containing pickled model")
    parser.add_argument("--annotated", dest="annotated", help="Output file for annotated data")
    args, rest = parser.parse_known_args()
