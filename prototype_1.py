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
import time # used to time the simulation
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
    probabilityDensity = (1 / bestGood.getPrice())
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

  #timesteps (Array of timesteps)
  #producers (Dictionary of profits)
  def plot_average_price(self, timesteps, producers):

    plots = [plt.plot(timesteps, profits) for profits in profits.values()]
    plt.legend( ('Producer 1', 'Producer 2'), loc=2)

    axes = plt.gca()
    axes.set_xlabel('Timestep')
    axes.set_ylabel('Profits')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    plt.show()

###############################################################################
# RUN METHOD
###############################################################################

  def run(self): 

    # just for debugging purposes
    def display_stats():
      print "\n"
      print "=================================================="
      print max(profits, key = lambda key: sum(profits[key])) + " Wins!\n"
      for producer in producers:
        print producer.getID() + " Profits: " + str(producer.getProfits())
        print producer.getID() + " Average Price: " + str(producer.getAverageGoodPrice())
        print producer.getID() + " Average Good Distance: " + str(abs(producer.getAverageGoodID() - (sum(goodsDemanded) / len(goodsDemanded))))
        print ""
      print "================================================="

    # initialize producers and arrays for plotting
    producers = [
      Producer('producer0', [Good(rd.random(), rd.random()) for good in range(self.numFactoryGoods)]),
      Producer('producer1', [Good(rd.random(), rd.random()) for good in range(self.numFactoryGoods)])
    ]
    profits = dict()
    profits['producer0'] = np.zeros(self.simLength + 1)
    profits['producer1'] = np.zeros(self.simLength + 1)

    #run simulations
    goodsDemanded = [] # keeping track of goods demanded
    for timestep in range(self.simLength):
      # print str(timestep), # print timesteps to console to observe progress
      for numConsumers in range(self.numConsumers):
        goodDemanded = rd.random() 
        goodsDemanded.append(goodDemanded)
        self.consumerBuysFrom(producers, goodDemanded)
      for producer in producers:
        profits[producer.getID()][timestep + 1] = producer.getProfits()

    #Does the producer with the most profits in the end also have the highest average price?
    averagePrices = dict()
    for producer in producers:
      averagePrices[producer.getID()] = producer.getAverageGoodPrice()

    if max(averagePrices, key = lambda key: averagePrices[key]) == max(profits, key = lambda key: sum(profits[key])):
      result = 1 # they both have the most profits and highest average good price
    else:
      result = 0 # they don't

    # display_stats()

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
  print ""
  print "================================================="
  print "Results:"
  #print str(results)
  print ""
  print str(sum(results) / len(results) * 100) + "%" + " of the time the producer with the most profits also had the highest average price"
  print ""
  print "Simulation took " + str(end - start) + " seconds to run!"
  print ""
  print "================================================="

display_results(50)