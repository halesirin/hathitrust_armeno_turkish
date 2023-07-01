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
    ("FOLDS", "", 1),
    ("N", "", 3),
    ("RANDOM_SEED", "", 0),
    ("TRAIN_PROPORTION", "", 0.8),
    ("DEV_PROPORTION", "", 0.1),
    ("TEST_PROPORTION", "", 0.1),    
    ("HATHITRUST_ROOT","", "/export/large_corpora/hathi_trust")
)

env = Environment(
    variables=vars,
    ENV=os.environ,
    tools=[steamroller.generate],
    
    BUILDERS={
        "FilterMarc" : Builder(
            action="python scripts/filter_marc.py --outputs ${TARGETS[0]} --hathitrust_root ${HATHITRUST_ROOT}"
        ),
        "FilterHathiMetadata" : Builder(
            action="python scripts/filter_hathi_metadata.py --output ${TARGETS[0]} --hathitrust_root ${HATHITRUST_ROOT}"
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
        "ApplyModel" : Builder(
            action="python scripts/apply_model.py --model ${SOURCES[0]} --annotated ${TARGETS[0]}"
        ),
        "GenerateReport" : Builder(
            action="python scripts/generate_report.py --annotated ${SOURCES[0]} --score_files ${SOURCES[1:]} --report ${TARGETS[0]}"
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
#
# Note how variables are specified in each invocation, and their values used to fill
# in the build commands *and* determine output filenames.  It's a very flexible system,
# and there are ways to make it less verbose, but in this case explicit is better than
# implicit.
#
# Note also how the outputs ("targets") from earlier invocation are used as the inputs
# ("sources") to later ones, and how some outputs are also gathered into the "results"
# variable, so they can be summarized together after each experiment runs.


filtered = env.FilterMarc(["work/subset_TA.json"],[]) 


