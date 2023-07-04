import argparse
import gzip

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
        Takes a list of input data files and concatenates them into a larger file.
        """
    )
    parser.add_argument("--inputs", dest="inputs", nargs="+", help="Input files")
    parser.add_argument("--output", dest="output", help="Output file")
    args, rest = parser.parse_known_args()

    with gzip.open(args.output, "wt") as ofd:
        for fname in args.inputs:
            with gzip.open(fname, "rt") as ifd:
                for line in ifd:
                    ofd.write(line)
