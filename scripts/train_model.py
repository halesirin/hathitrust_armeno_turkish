import argparse
import gzip
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", dest="data", help="Data input file")
    parser.add_argument("--train", dest="train", help="Train input file (list of line-numbers in the data file)")
    parser.add_argument("--dev", dest="dev", help="Dev input file (list of line-numbers in the data file)")
    parser.add_argument("--model", dest="model", help="Output file for pickled model")
    parser.add_argument("--scores", dest="scores", help="Output file for dev scores")
    parser.add_argument("--n", dest="n", default=3, type=int, help="Value of 'n', as in 'n-gram'")
    args, rest = parser.parse_known_args()

    # get lists of train/dev item-numbers
    train = []
    dev = []

    # initialize model
    model = {
        "armeno-turkish" : None,
        "non-armeno-turkish" : None
    }

    # train model and get dev instances
    devs = []
    with gzip.open(args.data, "rt") as ifd:
        for i, line in enumerate(ifd):
           j = json.loads(line)
           if i in train:
               # add counts from j["contents"] to the appropriate (sub)model
               pass
           elif i in dev:
               devs.append(j)
    
    # apply model
    guesses = []
    golds = []
    for j in devs:
        # apply both sub-models to j["content"], whichever is more likely is the "guess"
        #
        # guesses.append(guess)
        # golds.append(gold)
        pass

    # compute scores
    scores = {
        # "fscore" : sklearn.metrics.f_measure(...)
    }

    # save model
    with gzip.open(args.model, "wb") as ofd:
        ofd.write(pickle.dumps(model))

    # save scores
    with gzip.open(args.scores, "wb") as ofd:
        ofd.write(pickle.dumps(scores))
    
