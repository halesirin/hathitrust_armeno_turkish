import os
import os.path
import logging
import random
import subprocess
import shlex
import gzip
import re
import functools
import time
import imp
import sys
import json
import steamroller

# workaround needed to fix bug with SCons and the pickle module
del sys.modules['pickle']
sys.modules['pickle'] = imp.load_module('pickle', *imp.find_module('pickle'))
import pickle

# Variables control various aspects of the experiment.  Note that you have to declare
# any variables you want to use here, with reasonable default values, but when you want
# to change/override the default values, do so in the "custom.py" file.
vars = Variables("custom.py")
vars.AddVariables(
    ("OUTPUT_WIDTH", "", 5000),
    ("FOLDS", "", 5),
    ("N", "", 3),
    ("RANDOM_SEED", "", 0),
    ("TRAIN_PROPORTION", "", 0.8),
    ("DEV_PROPORTION", "", 0.1),
    ("TEST_PROPORTION", "", 0.1),    
    ("HATHITRUST_ROOT", "", "/export/large_corpora/hathi_trust")
)

env = Environment(
    variables=vars,
    ENV=os.environ,
    tools=[steamroller.generate],
    
    BUILDERS={
        "FilterMarc" : Builder(
            action="python scripts/filter_marc.py --output ${TARGETS[0]} --hathitrust_root ${HATHITRUST_ROOT}"
        ),
        "CollectionToJSON" : Builder(
            action="python scripts/collection_to_json.py --input ${SOURCES[0]} --output ${TARGETS[0]} --label ${LABEL}"
        ),
        "MergeEntries" : Builder(
            action="python scripts/merge_entries.py --inputs ${SOURCES} --output ${TARGETS[0]}"
        ),
        "ExpandEntries" : Builder(
            action="python scripts/expand_entries.py --input ${SOURCES[0]} --output ${TARGETS[0]} --hathitrust_root ${HATHITRUST_ROOT}"
        ),
        "RandomSplit" : Builder(
            action="python scripts/random_split.py --input ${SOURCES[0]} --outputs ${TARGETS} --proportions ${TRAIN_PROPORTION} ${DEV_PROPORTION} ${TEST_PROPORTION} --random_seed ${RANDOM_SEED}"
        ),
        "TrainModel" : Builder(
            action="python scripts/train_model.py --data ${SOURCES[0]} --train ${SOURCES[1]} --dev ${SOURCES[2]} --model ${TARGETS[0]} --scores ${TARGETS[1]} --n ${N}"
        ),
        "GenerateFinalCorpus" : Builder(
            action="python scripts/generate_final_corpus.py --to_annotate ${SOURCES[0]} --score_files ${SOURCES[1:]} --report ${TARGETS[0]} --corpus ${TARGETS[1]}"
        )
    }
)

armeno_turkish = env.CollectionToJSON(
    ["work/True_AT_set.jsonl.gz"],
    ["data/True_AT.tsv.gz"],
    LABEL="True"
)

non_armeno_turkish = env.CollectionToJSON(
    ["work/NAT_set.jsonl.gz"],
    ["data/Non_AT.tsv.gz"],
    LABEL="False"
) 

labeled = env.MergeEntries(
    ["work/labeled.jsonl.gz"],
    [armeno_turkish, non_armeno_turkish]
)

labeled_with_content = env.ExpandEntries(
    ["work/labeled_with_content.jsonl.gz"],
    [labeled]
)
data_lake = env.FilterMarc(
    ["work/data_lake.jsonl.gz"],
    [],
    REGEXES=[]
)

#data_lake_with_content = env.ExpandEntries(
#   ["work/data_lake_with_content.jsonl.gz"],
#   [data_lake]
#)

model_scores_pairs = []
for fold in range(1, env["FOLDS"] + 1):
    train, dev, test = env.RandomSplit(
        ["work/${FOLD}/train.jsonl.gz", "work/${FOLD}/dev.jsonl.gz", "work/${FOLD}/test.jsonl.gz"],
        [labeled_with_content],
        FOLD=fold,
        RANDOM_SEED=fold
    )
    for n in [2, 3, 4]:
        model, scores = env.TrainModel(
            ["work/${FOLD}/${N}/model.pkl.gz", "work/${FOLD}/${N}/scores.json"],
            [labeled_with_content, train, dev],
            N=n,
            FOLD=fold
        )
        model_scores_pairs.append((model, scores))
    

#env.GenerateFinalCorpus(
#    ["work/report.txt", "work/final_corpus.jsonl.gz"],
#    [data_lake_with_content] + model_scores_pairs
#)
