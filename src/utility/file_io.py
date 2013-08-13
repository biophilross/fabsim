###############################################################################
# IMPORT MODULES
###############################################################################

import json # for encoding and decoding data
import os   # interface with operating system

###############################################################################
# I/O METHODs
###############################################################################

# fileName (str)
# data (Dictionary)
def write_json(fileName, data):
  with open(fileName, 'w') as f:
    json.dump(data, f)

# fileName (str)
def read_json(fileName):
  if os.path.exists(fileName):
    with open(fileName, 'r') as f:
      return json.load(f)
  else:
    print('File does not exist!')