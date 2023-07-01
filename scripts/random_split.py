import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--outputs", dest="outputs", nargs=3, help="Output files")
    parser.add_argument("--proportions", dest="proportions", type=float, nargs=3, help="Proportions of data for train/dev/test")
    parser.add_argument("--random_seed", dest="random_seed", type=int, default=0)
    args, rest = parser.parse_known_args()
