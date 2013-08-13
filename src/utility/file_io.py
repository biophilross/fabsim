#!/usr/bin/env python

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators - PROTOTYPE
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

"""
This file contains all of the file input/output functions used
within validate.py and simulation.py. Currently it can only read and write
data in Javascript Object Notation (JSON) format.
"""


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
  "Opens a file and writes JSON formatted data to specified file."
  with open(fileName, 'w') as f:
    json.dump(data, f)

# fileName (str)
def read_json(fileName):
  "Reads JSON formatted data from an existing file."
  if os.path.exists(fileName):
    with open(fileName, 'r') as f:
      return json.load(f)
  else:
    print('File does not exist!')