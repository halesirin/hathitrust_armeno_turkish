import argparse
import warnings
import json
import pickle
import gzip
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
warnings.simplefilter("ignore")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", help="Input file of data to annotate")
    parser.add_argument("--model_scores_pairs", dest="model_scores_pairs", nargs="+", help="Input files of models and scores from experiments")
    parser.add_argument("--model", dest="model", help="Input file for model")
    parser.add_argument("--vectorizer", dest="vectorizer", help="Input file for vectorizer")
    parser.add_argument("--corpus", dest="corpus", help="Output file for final corpus")
    args, rest = parser.parse_known_args()

#Creating content and title lists
X = []
y = []
htids = []

with gzip.open(args.input, "rt") as ifd:
    for line in ifd:
        data = json.loads(line)
        tokens = (data['content']).lower().strip().split()
        sub_len = 1000
        num_subdocs = int(len(tokens)/sub_len)
        for subnum in range(num_subdocs):
            start = subnum * sub_len
            end = (subnum+1) * sub_len
            sub_tokens = tokens[start:end]
            sub_document = " ".join(sub_tokens)
            htid = data['htid']
            marc = data['marc']
            X.append(sub_document)
            htids.append(htid)
            
X_tuples = list(zip(X, htids))
X_content = [content for content, htid in X_tuples]
title_test = [htid for content, htid in X_tuples]

with gzip.open(args.vectorizer, "rb") as ifd:
    cv = pickle.loads(ifd.read())
    
#cv = pickle.load(open("vectorizer.pickle", "rb"))
X = cv.transform(X_content).toarray()


with gzip.open(args.model, "rb") as ifd:
    model = pickle.loads(ifd.read())
predicted = model.predict(X)

pr_dataset = []
for index, value in enumerate(predicted):
    if value == 1:
        pr_dataset.append(title_test[index])
        
with gzip.open(args.corpus, 'wt') as ofh:
    for line in pr_dataset:
        ofh.write(json.dumps(line)+"\n")
