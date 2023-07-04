import argparse
import gzip
import random

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
        Takes an input data file, a list of output file names, and a corresponding list of proportions.
        Shuffles the input lines, and splits them into the output files according to the proportions.

        Note: does not write the actual input lines to the output files, but instead writes the *line numbers*.
        This avoids duplicating large amounts of data, but means that the next script will need both the
        random split file *and* the original data file.

        All inputs/outputs are read/written with gzip compression.  A random seed may be specified for
        reproducibility.
        """
        )
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--outputs", dest="outputs", nargs="+", help="Output files")
    parser.add_argument("--proportions", dest="proportions", type=float, nargs="+", help="Proportions of data for each output file")
    parser.add_argument("--random_seed", dest="random_seed", type=int, default=None)
    args, rest = parser.parse_known_args()

    if len(args.outputs) != len(args.proportions):
        raise Exception("The number of output files and the number of proportions must be the same.")

    if sum(args.proportions) > 1 or any([x <= 0 for x in args.proportions]):
        raise Exception("The specified proportions must all be between 0 and 1, and sum to less than or equal to 1.")
    
    if args.random_seed:
        random.seed(args.random_seed)

    line_count = 0
    with gzip.open(args.input, "rt") as ifd:
        for line in ifd:
            line_count += 1

    line_numbers = list(range(line_count))
    random.shuffle(line_numbers)

    for prop, fname in zip(args.proportions, args.outputs):
        num = int(prop * line_count)
        with gzip.open(fname, "wt") as ofd:
            for line_num in line_numbers[:num]:
                ofd.write("{}\n".format(line_num))
            line_numbers = line_numbers[num:]
