import csv
import json
import argparse
import gzip

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output", help="Output file")
    parser.add_argument("--input", dest="input", help="Input file")
    args, rest = parser.parse_known_args()

    id_list = []
    with gzip.open(args.input, "rt") as ifd:
        cifd = csv.DictReader(ifd, delimiter="\t")
        for row in cifd:
            id_list.append((row["htid"]))

    with gzip.open(args.output, "w") as ofh:
        for item in id_list:
            j = {
                "htid": item
            }
            ofh.write(json.dumps(j)+"\n")
