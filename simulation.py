#!/usr/bin/env python

"""
###############################################################################
PROTOTYPE

Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators
Original Author: Wyman Zhao
Contributor(s): Philipp Ross

###############################################################################
"""

###############################################################################
# IMPORT MODULES
###############################################################################

from __future__ import division # will always return floating point
import goods
import producers 
import time                     # for timing the simulation
import json                     # for encoding and decoding data
import os                       # interface with operating system
import random as rd             # random number generator
import numpy as np              # numerical functionality
import matplotlib.pyplot as plt # plotting

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
  def __init__(self, simLength, numGoods, numConsumers, numProducers, percentFactory, factoryRate, fabricatorRate):
    print "Running..."
    print ""
    self.simLength = simLength
    self.numGoods = numGoods
    self.numConsumers = numConsumers
    self.numProducers = numProducers
    self.numFactoryGoods = int(numGoods * percentFactory)
    self.numFabricatorGoods = numGoods - self.numFactoryGoods
    self.factoryRate = factoryRate
    self.fabricatorRate = fabricatorRate

###############################################################################
# DECISION MAKING METHODS
###############################################################################

  #goodDemanded (float)
  #producer (Producer object)
  def calcProbDensity(self, producer, goodDemanded):
    bestGood = producer.getClosestTo(goodDemanded)
    if bestGood.getQuantity():
      probabilityDensity = (1 / (bestGood.getID() - goodDemanded)**2) * (1 / bestGood.getPrice())
    else: #there is no bestGood
      probabilityDensity = 0
    return probabilityDensity

  #producers (Array of Producers)
  def rouletteConsumerBuysFrom(self, producers, goodDemanded):
    #Roulette Wheel Selection
    producerProbabilities = [self.calcProbDensity(producer, goodDemanded) for producer in producers]
    sumOfProbabilities = sum(producerProbabilities)
    rouletteChoice = rd.random() * sumOfProbabilities
    currentChoice = 0
    bestProducer = producers[0]
    for producer in producers:
      #producer only contributes if quantity is greater than 0
      if producer.getClosestTo(goodDemanded).getQuantity() > 0:
        currentChoice = currentChoice + self.calcProbDensity(producer, goodDemanded)
        if(currentChoice >= rouletteChoice):
          bestProducer = producer
          break
    if(currentChoice >= rouletteChoice):
      bestGood = bestProducer.getClosestTo(goodDemanded)
      bestProducer.sell(bestGood)

  #producers (Array of Producers)
  def consumerBuysFrom(self, producers, goodDemanded):
    producerProbabilities = [self.calcProbDensity(producer, goodDemanded) for producer in producers]
    sumOfProbabilities = sum(producerProbabilities)
    if sumOfProbabilities > 0:
      normalizedProbabilities = [{ 
          "producer"    : producer,
          "probability" : self.calcProbDensity(producer, goodDemanded) / sumOfProbabilities
        } for producer in producers]
      bestProducer = max(normalizedProbabilities, key = lambda value: value['probability'])['producer']
      bestGood = bestProducer.getClosestTo(goodDemanded)
      bestProducer.sell(bestGood)

###############################################################################
# RUN METHOD
###############################################################################

  def run(self, scenario): 
    # scenario = 'factories', 'fabricators' or 'all'

    # for debugging purposes
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

    # initialize producers and arrays for plotting based on  scenario
    producers = []
    profits = dict()
    if scenario == 'factories':
      for i in range(self.numProducers):
        inventory = [Good(rd.random(), rd.random(), self.factoryRate) for good in range(self.numFactoryGoods)] # set inventory
        key = 'factory' + str(i) # set key and id
        producers.append(Producer(inventory, self.factoryRate, key))
        profits[key] = np.zeros(self.simLength + 1)
    elif scenario == 'fabricators':
      for i in range(self.numProducers):
        inventory = [Good(rd.random(), rd.random(), self.fabricatorRate) for good in range(self.numFabricatorGoods)] # set inventory
        key = 'fabricator' + str(i) # set key and id
        producers.append(Producer(inventory, self.fabricatorRate, key))
        profits[key] = np.zeros(self.simLength + 1)
    elif scenario == 'all':
      for i in range(int(self.numProducers / 2)):
        inventory = [Good(rd.random(), rd.random(), self.factoryRate) for good in range(self.numFactoryGoods)] # set inventory
        key = 'factory' + str(i) # set key and id
        producers.append(Producer(inventory, self.factoryRate, key))
        profits[key] = np.zeros(self.simLength + 1)
      for i in range(int(self.numProducers / 2)):
        inventory = [Good(rd.random(), rd.random(), self.fabricatorRate) for good in range(self.numFabricatorGoods)] # set inventory
        key = 'fabricator' + str(i) # set key and id
        producers.append(Producer(inventory, self.fabricatorRate, key))
        profits[key] = np.zeros(self.simLength + 1)

    #run simulations
    goodsDemanded = [] # keeping track of goods demanded
    for timestep in range(self.simLength):
      print str(timestep), # print time steps to console to observe progress
      for numConsumers in range(self.numConsumers):
        goodDemanded = rd.random()
        goodsDemanded.append(goodDemanded)
        self.consumerBuysFrom(producers, goodDemanded)
      for producer in producers:
        producer.updateInventory()
        profits[producer.getID()][timestep + 1] = producer.getProfits()

    #Does the producer with the most profits in the end also have the highest average price?
    averagePrices = dict()
    for producer in producers:
      averagePrices[producer.getID()] = producer.getAverageGoodPrice()

    if max(averagePrices, key = lambda key: averagePrices[key]) == max(profits, key = lambda key: sum(profits[key])):
      result = 1 # they both have the most profits and highest average good price
    else:
      result = 0 # they don't

    display_stats()

    return result

###############################################################################
# RUN SIM
###############################################################################

SIMLENGTH = 100
NUMGOODS = 1000
NUMCONSUMERS = 1000
NUMPRODUCERS = 2
PERCENTFACTORY = 0.1
FACTORYRATE = 10
FABRICATORRATE = 1
sim = simulation(SIMLENGTH, NUMGOODS, NUMCONSUMERS, NUMPRODUCERS, PERCENTFACTORY, FACTORYRATE, FABRICATORRATE)


# Use this function to display the results of multiple simulation runs
#numSimulations (int)
def display_results(numSimulations):
  start = time.clock() # timing how long the simulation takes to run
  factory_results = []
  fabricator_results = []
  all_results = []
  for i in range(numSimulations):
    factory_results.append(sim.run('factories'))
    fabricator_results.append(sim.run('fabricators'))
    all_results.append(sim.run('all'))
  end = time.clock() # timing how long the simulation takes to run
  print "Input parameters are:"
  print ""
  print "SIMLENGTH = {simLength}\nNUMGOODS = {numGoods}\nNUMCONSUMERS = {numConsumers}\nNUMPRODUCERS = {numProducers}\nPERCENTFACTORY = {percentFactory}\nFACTORYRATE = {factoryRate}\nFABRICATORRATE = {fabricatorRate}".format(
    simLength = SIMLENGTH, 
    numGoods = NUMGOODS, 
    numConsumers = NUMCONSUMERS, 
    numProducers = NUMPRODUCERS, 
    percentFactory = PERCENTFACTORY, 
    factoryRate = FACTORYRATE, 
    fabricatorRate = FABRICATORRATE
  )
  print ""
  print "================================================="
  print "Factory Results:"
  print str(factory_results)
  print str(sum(factory_results) / len(factory_results) * 100) + "%"
  print ""
  print "================================================="
  print "Fabricator Results:"
  print str(fabricator_results)
  print str(sum(fabricator_results) / len(fabricator_results) * 100) + "%"
  print ""
  print "================================================="
  print "All Results:"
  print str(all_results)
  print str(sum(all_results) / len(all_results) * 100) + "%"
  print "================================================="
  print ""
  print "Simulation took " + str(end - start) + " seconds to run!"
  print "================================================="
