import csv
import json
import argparse
import gzip

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output", help="Output file")
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--label", dest="label", help="Label")
    args, rest = parser.parse_known_args()

    item_list = []
    with gzip.open(args.input, "rt") as ifd:
        cifd = csv.DictReader(ifd, delimiter="\t")
        for row in cifd:
            item_list.append(row)

    with gzip.open(args.output, "wt") as ofh:
        for item in item_list:
            j = {
                "htid": item["htid"],
                "label": args.label,
                "ht_meta":item 
            }
            ofh.write(json.dumps(j)+"\n")
