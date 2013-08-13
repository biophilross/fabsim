#!/usr/bin/env python

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators - PROTOTYPE
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

"""
This file contains the Good class imported by validate.py and simulation.py in order
to instantiate Good objects.
"""

###############################################################################
# DEFINE GOOD CLASS
###############################################################################

class Good:
  """Class for Good objects."""
  #idInput (float)
  #priceInput (float)
  #quantityInput(int)
  def __init__(self, idInput, priceInput):
    # set good ID used to differentiate goods
    self.goodID = idInput
    # set good price
    self.price = priceInput

  def getID(self):
    """Returns the goodID of a good."""
    return self.goodID

  def getPrice(self):
    """Returns the price of a good."""
    return self.price