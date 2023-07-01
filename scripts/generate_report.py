import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--annotated", dest="annotated", help="Input file of annotated data")
    parser.add_argument("--score_files", dest="score_files", nargs="+", help="Input files of scores from experiments")
    parser.add_argument("--report", dest="report", help="Output file for report")
    args, rest = parser.parse_known_args()
