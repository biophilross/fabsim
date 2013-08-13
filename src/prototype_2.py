#!/usr/bin/env python

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
import random as rd             # random number generator
import numpy as np              # numerical functionality
import matplotlib.pyplot as plt # plotting

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
  #numProducers (int)
  def __init__(self, simLength, numGoods, numConsumers, numProducers):
    print "Running..."
    print ""
    self.simLength = simLength
    self.numGoods = numGoods
    self.numConsumers = numConsumers
    self.numProducers = numProducers

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
  def plot(self, producers):

    # format data
    producerIDs = [int(producer['producerID']) for producer in producers]
    profits = [producer['profits'] for producer in producers]
    average_prices = [producer['average_price'] for producer in producers]
    average_distances = [producer['average_distance'] for producer in producers]

    # determine figure size - figsize(1,1) = 1" x 1" or 80 pixels x 80 pixels
    plt.figure(1, figsize=(12, 8))

    # plot profits
    plt.subplot(221)
    plt.grid(True)
    plt.title('Profits')
    plt.ylabel('Profits')
    plt.xlabel('ProducerIDs')
    plt.axis([0, len(producerIDs) - 1 , 0, max(profits)])
    plt.fill_between(producerIDs, profits, alpha='0.6', color='blue')
    plt.plot(producerIDs, profits, 'k')

    # plot average_prices
    plt.subplot(222)
    plt.grid(True)
    plt.title('Average Good Price')
    plt.ylabel('Average Price')
    plt.xlabel('ProducerIDs')
    plt.axis([0, len(producerIDs) - 1, 0, 1])
    plt.fill_between(producerIDs, average_prices, alpha='0.6', color='blue')
    plt.plot(producerIDs, average_prices, 'k')

    # plot average_distances
    plt.subplot(223)
    plt.grid(True)
    plt.title('Average Good Distance')
    plt.ylabel('Distance')
    plt.xlabel('ProducerIDs')
    plt.axis([0, len(producerIDs) - 1, 0, 1])
    plt.fill_between(producerIDs, average_distances, alpha='0.6', color='blue')
    plt.plot(producerIDs, average_distances, 'k')

    # display plot
    plt.tight_layout()
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

  def run(self, numTrials = 1, debug=False): # add numSims as input?

    start = time.clock() # timing how long the simulation takes to run

    # initialize producers and arrays for plotting
    profits = dict()
    producers = []
    goodIDs = [rd.random() for i in range(self.numGoods)]
    for i in range(self.numProducers):
      key = 'producer_' + str(i)
      inventory = [Good(goodIDs[i], rd.random()) for i in range(self.numGoods)]
      producers.append(Producer(key, inventory))
      profits[key] = np.zeros(self.simLength + 1)

    # run simulations
    goodsDemanded = [] # keeping track of goods demanded
    for timestep in range(self.simLength):
      goodDemanded = rd.random()
      goodsDemanded.append(goodDemanded)
      for numConsumers in range(self.numConsumers):
        self.consumerBuysFrom(producers, goodDemanded)
      for producer in producers:
        profits[producer.getID()][timestep + 1] = producer.getProfits()

    # calculate the average good demanded
    averageGoodDemanded = sum(goodsDemanded) / len(goodsDemanded)

    #Write results to file in JSON format
    data = [{
      "producerID"       : producer.getID().split('_')[-1], # retrieve only the numerical characters
      "profits"          : producer.getProfits(),
      "average_price"    : producer.getAverageGoodPrice(),
      "average_distance" : abs(producer.getAverageGoodID() - averageGoodDemanded),
    self.write_json('results/p2_results.json', data)

    end = time.clock() # timing how long the simulation takes to run

    # if you want to look at the results of each simulation run individually
    if debug == True:
      print "\n"
      print "=================================================="
      print max(profits, key = lambda key: sum(profits[key])) + " Wins!\n"
      print "Average Good Demanded: " + str(averageGoodDemanded) + "\n"
      for producer in producers:
        print producer.getID() + " Profits: " + str(producer.getProfits())
        print producer.getID() + " Average Price: " + str(producer.getAverageGoodPrice())
        print producer.getID() + " Average Good Distance: " + str(abs(producer.getAverageGoodID() - (averageGoodDemanded)))
        print ""
      print "Simulation took " + str(end - start) + " seconds to run!"
      print ""
      print "================================================="

    # plot results 
    self.plot(data)

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

SIMLENGTH = 1000
NUMGOODS = 100
NUMCONSUMERS = 1000
NUMPRODUCERS = 20
PERCENTFACTORY = 0.1
sim = simulation(SIMLENGTH, NUMGOODS, NUMCONSUMERS, NUMPRODUCERS, PERCENTFACTORY)

sim.run(debug=True)

def display_results(numSimulations):
  start = time.clock() # timing how long the simulation takes to run
  results = []
  for i in range(numSimulations):
    results.append(sim.run())
  end = time.clock() # timing how long the simulation takes to run
  print "Input parameters are:"
  print ""
  print "SIMLENGTH = {simLength}\nNUMGOODS = {numGoods}\nNUMCONSUMERS = {numConsumers}\nNUMPRODUCERS = {numProducers}\nPERCENTFACTORY = {percentFactory}".format(
    simLength = SIMLENGTH, 
    numGoods = NUMGOODS, 
    numConsumers = NUMCONSUMERS, 
    numProducers = NUMPRODUCERS,
    percentFactory = PERCENTFACTORY
  )
  print "================================================="
  print ""
  print "Results:"
  print ""
  print str(sum(results) / len(results) * 100) + "%" + " of the time the producer with the most profits also had the lowest price for the good closest to the average demanded good"
  print ""
  print "Simulation took " + str(end - start) + " seconds to run!"
  print ""
  print "================================================="