import argparse
import gzip
#
# This script does *nothing* except print out its arguments and touch any files
# specified as outputs (thus fulfilling a build system's requirements for
# success).
#
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", dest="outputs", nargs="+", help="Output files")
    parser.add_argument("--hathitrust_root", dest="hathitrust_root")
    args, rest = parser.parse_known_args()
    
    with gzip.open(args.hathitrust_root+"/full_marc.json.gz") as ifd:
        print(args.hathitrust_root)
    """
    print("Building files {} from arguments {}".format(args.outputs, rest))
    for fname in args.outputs:
        with open(fname, "wt") as ofd:
            pass
    """
