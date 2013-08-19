#!/usr/bin/env python

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators - PROTOTYPE
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

"""
This file contains the Producer class imported by validate.py and simulation.py
in order to instantiate Producer objects.
"""

###############################################################################
# DEFINE PRODUCER CLASS
###############################################################################

class Producer:
  "Class for producer objects."
  #inventory (Array of Goods)
  #rate (int)
  #id (string)
  def __init__(self, idInput, inventoryInput):
    # set the inventory - made up of an array of Good objects
    self.inventory = inventoryInput
    # set producerID to easily distinguish producers
    self.producerID = idInput
    # set initial profits to zero
    self.profits = 0

  def getID(self):
    "Returns the unique producerID."
    return self.producerID

  def getInventory(self):
    "Returns the inventory of a producer."
    return self.inventory

  def getProfits(self):
    "Returns the current profits of a producer."
    return self.profits

  def getAverageGoodPrice(self):
    "Returns the average price of the goods in a producer's inventory."
    prices = [good.getPrice() for good in self.getInventory()]
    return sum(prices) / len(self.getInventory())

  def getAverageGoodID(self):
    "Returns the average goodID of the goods in a producer's inventory."
    ids = [good.getID() for good in self.getInventory()]
    return sum(ids) / len(self.getInventory())

  #currentGoods (Array of Goods)
  #goodDemanded (float)
  def getClosestTo(self, currentGoods, goodDemanded):
    """Returns the good with the goodID closest to the goodDemanded by a consumer."""
    return min(currentGoods, key = lambda good: abs(goodDemanded - good.getID()))

  #good (Good object)
  def sell(self, good):
    """Updates the producer's profits by the price of the good being sold to a consumer."""
    if good in self.getInventory():
      self.profits = self.profits + good.getPrice()

  def __repr__(self):
    """Returns code representation of the instance."""
    return "Producer ID: %r\n %r" % (self.getID(), self.getInventory())

  def __str__(self):
    """Returns string representation of the instance."""
    return "Producer ID: %r\n %r" % (self.getID(), self.getInventory())