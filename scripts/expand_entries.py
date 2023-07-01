import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--output", dest="output", help="Output file")
    parser.add_argument("--hathitrust_root", dest="hathitrust_root", help="Path to HathiTrust")
    args, rest = parser.parse_known_args()
