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
            action="python scripts/collection_to_json.py --output ${TARGETS[0]} --hathitrust_root ${HATHITRUST_ROOT}"
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
            action="python scripts/train_model.py --train ${SOURCES[0]} --dev ${SOURCES[1]} --test ${SOURCES[2]} --model ${TARGETS[0]} --scores ${TARGETS[1]} --n ${N}"
        ),
        "GenerateFinalCorpus" : Builder(
            action="python scripts/generate_final_corpus.py --to_annotate ${SOURCES[0]} --score_files ${SOURCES[1:]} --report ${TARGETS[0]} --corpus ${TARGETS[1]}"
        )
    }
)

# OK, at this point we have defined all the builders and variables, so it's
# time to specify the actual experimental process, which will involve
# running all combinations of datasets, folds, model types, and parameter values,
# collecting the build artifacts from applying the models to test data in a list.
#
# The basic pattern for invoking a build rule is:
#
#   "Rule(list_of_targets, list_of_sources, VARIABLE1=value, VARIABLE2=value...)"
# Note how variables are specified in each invocation, and their values used to fill
# in the build commands *and* determine output filenames.  It's a very flexible system,
# and there are ways to make it less verbose, but in this case explicit is better than
# implicit.
#
# Note also how the outputs ("targets") from earlier invocation are used as the inputs
# ("sources") to later ones, and how some outputs are also gathered into the "results"
# variable, so they can be summarized together after each experiment runs.


armeno_turkish = env.CollectionToJSON(
    ["work/True_AT_set.json"],
    ["data/True_AT.tsv.gz"],
    REGEXES=[]
)

non_armeno_turkish = env.CollectionToJSON(
    ["work/NAT_set.json"],
    ["data/Non_AT.tsv.gz"],
    REGEXES=[]
) 

labeled = env.MergeEntries(
    ["work/labeled.jsonl.gz"],
    [armeno_turkish, non_armeno_turkish]
)

full_labeled = env.ExpandEntries(
    ["work/full_labeled.jsonl.gz"],
    [labeled]
)
data_lake = env.FilterMarc(
    ["work/data_lake.jsonl.gz"],
    [],
    REGEXES=[]
)

full_data_lake = env.ExpandEntries(
    ["work/full_data_lake.jsonl.gz"],
    [data_lake]
)

model_scores_pairs = []
for fold in range(1, env["FOLDS"] + 1):
    train, dev, test = env.RandomSplit(
        ["work/${FOLD}/train.jsonl.gz", "work/${FOLD}/dev.jsonl.gz", "work/${FOLD}/test.jsonl.gz"],
        [full_labeled],
        FOLD=fold,
        RANDOM_SEED=fold
    )
    for n in [2, 3, 4]:
        model, scores = env.TrainModel(
            ["work/${FOLD}/${N}/model.pkl.gz", "work/${FOLD}/${N}/scores.json"],
            [train, dev, test],
            N=n,
            FOLD=fold
        )
        model_scores_pairs.append((model, scores))

env.GenerateFinalCorpus(
    ["work/report.txt", "work/final_corpus.jsonl.gz"],
    [full_data_lake] + model_scores_pairs
)
