"""
###############################################################################
PROTOTYPE

Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators
Original Author: Wyman Zhao
Contributor(s): Philipp Ross

###############################################################################
CONTENTS

IMPORT MODULES
GOOD CLASS
PRODUCER CLASS
SIMULATION CLASS
RUN SIM
###############################################################################
"""

###############################################################################
# IMPORT MODULES
###############################################################################

from __future__ import division # will always return floating point
import time                     # for timing the simulation
import json                     # for encoding and decoding data
import os                       # interface with operating system
import random as rd
import numpy as np
import matplotlib.pyplot as plt

###############################################################################
# DEFINE GOOD CLASS
###############################################################################

class Good:
  #idInput (float)
  #priceInput (float)
  #quantityInput(int)
  def __init__(self, idInput, priceInput):
    self.goodID = idInput
    self.price = priceInput

  def getID(self):
    return self.goodID

  def getPrice(self):
    return self.price

###############################################################################
# DEFINE PRODUCER CLASS
###############################################################################

class Producer:
  #inventory (Array of Goods)
  #rate (int)
  #id (string)
  def __init__(self, idInput, inventoryInput):
    self.inventory = inventoryInput
    self.producerID = idInput
    self.profits = 0

  def getID(self):
    return self.producerID

  def getInventory(self):
    return self.inventory

  def getProfits(self):
    return self.profits

  def getAverageGoodPrice(self):
    prices = [good.getPrice() for good in self.getInventory()]
    return sum(prices) / len(self.getInventory())

  def getAverageGoodID(self):
    ids = [good.getID() for good in self.getInventory()]
    return sum(ids) / len(self.getInventory())

  #currentGoods (Array of Goods)
  #goodDemanded (float)
  def getClosestTo(self, currentGoods, goodDemanded):
    return min(currentGoods, key = lambda good: abs(goodDemanded - good.getID()))

  #good (Good object)
  def sell(self, good):
    if good in self.inventory:
      self.profits = self.profits + good.getPrice()

  def __str__(self):
    for good in self.inventory:
      print "GoodID: " + str(good.getID()) + " Price: " + str(good.getPrice()) + "\n"

###############################################################################
# DEFINE SIMULATION CLASS
###############################################################################

class simulation:
  #simLength (int)
  #numGoods (int)
  #numConsumers (int)
  #percentFactory (float) between 0 and 1
  #factoryRate (int)
  #fabricatoryRate (int)
  def __init__(self, simLength, numGoods, numConsumers, percentFactory):
    print "Running..."
    print ""
    self.simLength = simLength
    self.numGoods = numGoods
    self.numConsumers = numConsumers
    self.numFactoryGoods = int(numGoods * percentFactory)
    self.numFabricatorGoods = numGoods - self.numFactoryGoods

###############################################################################
# DECISION MAKING METHODS
###############################################################################

  #goodDemanded (float)
  #producer (Producer object)
  def calcProbDensity(self, producer, goodDemanded):
    bestGood = producer.getClosestTo(producer.getInventory(), goodDemanded)
    probabilityDensity = (1 / (bestGood.getID() - goodDemanded)**2) * (1 / bestGood.getPrice())
    return probabilityDensity

  #producers (Array of Producers)
  def consumerBuysFrom(self, producers, goodDemanded):
    producerProbabilities = [{ 
    "producer"    : producer, 
    "probability" : self.calcProbDensity(producer, goodDemanded)
    } for producer in producers]
    maxProbability = max(producerProbabilities, key = lambda key: key['probability'])
    bestProducer = maxProbability['producer']
    bestGood = bestProducer.getClosestTo(bestProducer.getInventory(), goodDemanded)
    bestProducer.sell(bestGood)

###############################################################################
# PLOTTING METHODs
###############################################################################

  #producers (List of Dictionaries of Producers)
  def plot_histogram(self, producers):

    producerIDs = [producer['producerID'] for producer in producers]
    profits = [producer['profits'] for producer in producers]
    average_prices = [producer['average_price'] for producer in producers]
    average_distances = [producer['average_distance'] for producer in producers]

    hist, bins = np.histogram(profits, bins = 2)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.show()

###############################################################################
# I/O METHODs
###############################################################################

  def write_json(self, fileName, data):
    with open(fileName, 'w') as f:
      json.dump(data, f)

  def read_json(self, fileName):
    if os.path.exists(fileName):
      with open(fileName, 'r') as f:
        return json.load(f)
    else:
      print('File does not exist!')

###############################################################################
# RUN METHOD
###############################################################################

  def run(self): 

    # just for debugging purposes
    def display_stats():
      print "\n"
      print "=================================================="
      print max(profits, key = lambda key: sum(profits[key])) + " Wins!\n"
      print "Average Good Demanded: " + str(averageGoodDemanded) + "\n"
      for producer in producers:
        print producer.getID() + " Profits: " + str(producer.getProfits())
        print producer.getID() + " Average Price: " + str(producer.getAverageGoodPrice())
        print producer.getID() + " Price Closest to Average Good Demanded: " + str(producer.getClosestTo(producer.getInventory(), averageGoodDemanded).getPrice())
        print producer.getID() + " Average Good Distance: " + str(abs(producer.getAverageGoodID() - (averageGoodDemanded)))
        print ""
      print "================================================="

    # initialize producers and arrays for plotting
    goodIDs = [rd.random() for i in range(self.numFabricatorGoods)]
    producers = [
      Producer('producer0', [Good(goodIDs[i], rd.random()) for i in range(self.numFactoryGoods)]),
      Producer('producer1', [Good(goodIDs[i], rd.random()) for i in range(self.numFactoryGoods)])
    ]
    profits = dict()
    profits['producer0'] = np.zeros(self.simLength + 1)
    profits['producer1'] = np.zeros(self.simLength + 1)

    # run simulations
    goodsDemanded = [] # keeping track of goods demanded
    for timestep in range(self.simLength):
      print str(timestep), # print time steps to console to observe progress
      for numConsumers in range(self.numConsumers):
        goodDemanded = rd.random()
        goodsDemanded.append(goodDemanded)
        self.consumerBuysFrom(producers, goodDemanded)
      for producer in producers:
        profits[producer.getID()][timestep + 1] = producer.getProfits()

    # calculate the average good demanded
    averageGoodDemanded = sum(goodsDemanded) / len(goodsDemanded)

    #Write results to file in JSON format
    data = [{
      "producerID"       : producer.getID(),
      "profits"          : producer.getProfits(),
      "average_price"    : producer.getAverageGoodPrice(),
      "average_distance" : abs(producer.getAverageGoodID() - (sum(goodsDemanded) / len(goodsDemanded)))
    } for producer in producers]

    display_stats()
    #self.plot_histogram(data)


    # The producer selling the good closest to the average good demanded for the cheapest - does he have the most profits?
    averagePrices = dict()
    for producer in producers:
      averagePrices[producer.getID()] = producer.getClosestTo(producer.getInventory(), averageGoodDemanded).getPrice()

    if min(averagePrices, key = lambda key: averagePrices[key]) == max(profits, key = lambda key: sum(profits[key])):
      result = 1 # they do
    else:
      result = 0 # they don't

    return result

###############################################################################
# RUN SIM
###############################################################################

SIMLENGTH = 100
NUMGOODS = 100
NUMCONSUMERS = 1000
PERCENTFACTORY = 0.1
sim = simulation(SIMLENGTH, NUMGOODS, NUMCONSUMERS, PERCENTFACTORY)

def display_results(numSimulations):
  start = time.clock() # timing how long the simulation takes to run
  results = []
  for i in range(numSimulations):
    results.append(sim.run())
  end = time.clock() # timing how long the simulation takes to run
  print "Input parameters are:"
  print ""
  print "SIMLENGTH = {simLength}\nNUMGOODS = {numGoods}\nNUMCONSUMERS = {numConsumers}\nPERCENTFACTORY = {percentFactory}".format(
    simLength = SIMLENGTH, 
    numGoods = NUMGOODS, 
    numConsumers = NUMCONSUMERS, 
    percentFactory = PERCENTFACTORY
  )
  print "================================================="
  print ""
  print "Results:"
  #print str(results)
  print ""
  print str(sum(results) / len(results) * 100) + "%" + " of the time the producer with the most profits also had the highest average price"
  print ""
  print "Simulation took " + str(end - start) + " seconds to run!"
  print ""
  print "================================================="

display_results(50)