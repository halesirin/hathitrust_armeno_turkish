import argparse
import pickle
import gzip
import json

def split_text(text, max_length):
    while len(text) > max_length:
        yield text[:max_length]
        text = text[max_length:]
    if len(text) > 0:
        yield text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", dest="data", help="Data input file")
    parser.add_argument("--train", dest="train", help="Train input file (list of line-numbers in the data file)")
    parser.add_argument("--dev", dest="dev", help="Dev input file (list of line-numbers in the data file)")
    parser.add_argument("--model", dest="model", help="Output file for pickled model")
    parser.add_argument("--scores", dest="scores", help="Output file for dev scores")
    parser.add_argument("--n", dest="n", default=3, type=int, help="Value of 'n', as in 'n-gram'")
    parser.add_argument("--max_length", dest="max_length", default=0, type=int, help="Max length of texts to evaluate on")
    args, rest = parser.parse_known_args()

    # Get lists of train/dev item-numbers
    train = []
    dev = []

    with gzip.open(args.train, "rt") as ifd:
        for line in ifd:
            train.append(json.loads(line))

    with gzip.open(args.dev, "rt") as ifd:
        for line in ifd:
            dev.append(json.loads(line))            

    models = {}

    # Train model and get dev instances
    devs = []
    with gzip.open(args.data, "rt") as ifd:
        for i, line in enumerate(ifd):
           j = json.loads(line)
           if i in train:
               label = j["label"]
               # Initialize model for this label if one doesn't exist yet
               # models[label] = models.get(label, None)
               
               # Add counts from j["contents"] to the model[label]
               # ...
               pass
           elif i in dev:
               devs.append(j)
    
    # Apply models to (chunks of) dev
    guesses = []
    golds = []
    for j in devs:
        gold = j["label"]
        # Apply models to j["content"], whichever is more likely is the "guess"
        #
        for chunk in (j["content"] if args.max_length == 0 else split_text(j["content"], args.max_length)):
            # guesses.append(guess)
            golds.append(gold)
            pass

    # compute scores
    scores = {
        # "fscore" : sklearn.metrics.f_measure(...)
    }

    # save model
    with gzip.open(args.model, "wb") as ofd:
        ofd.write(pickle.dumps(models))

    # save scores
    with gzip.open(args.scores, "wb") as ofd:
        ofd.write(pickle.dumps(scores))
