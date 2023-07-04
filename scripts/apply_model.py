import argparse
import gzip
import pickle
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", dest="data", help="Data input file")
    parser.add_argument("--model", dest="model", help="Input file containing pickled model")
    parser.add_argument("--annotated", dest="annotated", help="Output file for annotated data")
    args, rest = parser.parse_known_args()

    with gzip.open(args.model, "rb") as ifd:
        model = pickle.loads(ifd.read())

    with gzip.open(args.data, "rt") as ifd, gzip.open(args.annotated, "wt") as ofd:
        for line in ifd:
            j = json.loads(line)
            # apply model to j["contents"] and set j["guess"]
            # ...
            ofd.write(json.dumps(j) + "\n")
