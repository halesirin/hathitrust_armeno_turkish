import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train", dest="train", help="Train input file")
    parser.add_argument("--dev", dest="dev", help="Dev input file")
    parser.add_argument("--test", dest="test", help="Test input file")
    parser.add_argument("--model", dest="model", help="Output file for pickled model")
    parser.add_argument("--scores", dest="scores", help="Output file for dev and test scores")
    parser.add_argument("--n", dest="n", default=3, type=int, help="Value of 'n', as in 'n-gram'")
    args, rest = parser.parse_known_args()
