import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--to_annotate", dest="to_annotate", help="Input file of data to annotate")
    parser.add_argument("--model_scores_pairs", dest="model_scores_pairs", nargs="+", help="Input files of models and scores from experiments")
    parser.add_argument("--report", dest="report", help="Output file for report")
    parser.add_argument("--corpus", dest="corpus", help="Output file for final corpus")
    args, rest = parser.parse_known_args()
