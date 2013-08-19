#!/usr/bin/env python

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators - PROTOTYPE
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

"""
This file contains a special Validate class used just to validate the mathematical
model being tested out on TWO producers. It's very similar to the Simulation class.
The only thing differentiating producers here is the amount of goods in their inventory.
Other options included here that cannot be found explicitly in simulation.py include
explicitly choosing a test case and a buying decision function.
In addition there is no plotting functionality included.
"""

###############################################################################
# IMPORT MODULES
###############################################################################

from __future__ import division # will always return floating point
import time                     # for timing the simulation
import random as rd             # random number generator
import numpy as np              # numerical functionality

# import custom-made modules
from good import Good
from producer import Producer
from utility.file_io import read_json, write_json


###############################################################################
# DEFINE SIMULATION CLASS
###############################################################################

class Validate:
  "Class used to validate simulation models."
  #simLength (int)
  #numGoods (int)
  #numConsumers (int)
  def __init__(self, simLength, numGoods, numConsumers, percentFactory):
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

  # producers (Array of Producers)
  # goodDemanded (float)
  def nonRoulette(self, producers, goodDemanded):
    producerProbabilities = [{
    "producer"    : producer,
    "probability" : self.calcProbDensity(producer, goodDemanded)
    } for producer in producers]
    maxProbability = max(producerProbabilities, key = lambda key: key['probability'])
    bestProducer = maxProbability['producer']
    bestGood = bestProducer.getClosestTo(bestProducer.getInventory(), goodDemanded)
    bestProducer.sell(bestGood)

  # producers (Array of Producers)
  # goodDemanded (float)
  def roulette(self, producers, goodDemanded):
    #Roulette Wheel Selection
    producerProbabilities = [self.calcProbDensity(producer, goodDemanded) for producer in producers]
    sumOfProbabilities = sum(producerProbabilities)
    rouletteChoice = rd.random() * sumOfProbabilities
    currentChoice = 0
    bestProducer = producers[0]
    for producer in producers:
      currentChoice = currentChoice + self.calcProbDensity(producer, goodDemanded)
      if(currentChoice >= rouletteChoice):
        bestProducer = producer
        break
    if(currentChoice >= rouletteChoice):
      bestGood = bestProducer.getClosestTo(bestProducer.getInventory(), goodDemanded)
      bestProducer.sell(bestGood)

  # producers (Array of Producers)
  # goodDemanded (float)
  # function (str)
  def consumerBuysFrom(self, producers, goodDemanded, buyingDecision):
    if buyingDecision == 'roulette':
      return self.roulette(producers, goodDemanded)
    elif buyingDecision == 'nonRoulette':
      return self.nonRoulette(producers, goodDemanded)


###############################################################################
# MONITORSIM METHOD
###############################################################################

  def monitorSim(self, producers, profits, averageGoodDemanded, startSim, endSim, trial):
    print "=================================================="
    print max(profits, key = lambda key: sum(profits[key])) + " Wins!\n"
    print "Average Good Demanded: " + str(averageGoodDemanded) + "\n"
    for producer in producers:
      print producer.getID() + " Profits: " + str(producer.getProfits())
      print producer.getID() + " Average Price: " + str(producer.getAverageGoodPrice())
      print producer.getID() + " Average Good Distance: " + str(abs(producer.getAverageGoodID() - (averageGoodDemanded)))
      print ""
    print "Simulation " + str(trial + 1) + " took " + str(endSim - startSim) + " seconds to run!"
    print ""


###############################################################################
# INITIALIZE PRODUCERS METHOD
###############################################################################

  # testCase (str)
  # scenario (Str)
  def initialize_producers(self, testCase, scenario):
    """Initializes distinct producers based on the scenario given as an input."""
    # initialize keys and number of goods based on scenario
    if scenario == 'factories':
      keys            = ['factory_0', 'factory_1']
      inventoryGoods  = [self.numFactoryGoods, self.numFactoryGoods]
      goodConstants   = [[rd.random() for i in range(self.numFactoryGoods)], [rd.random() for i in range(self.numFactoryGoods)]]
    elif scenario == 'fabricators':
      keys            = ['fabricator_0', 'fabricator_1']
      inventoryGoods  = [self.numFabricatorGoods, self.numFabricatorGoods]
      goodConstants   = [[rd.random() for i in range(self.numFabricatorGoods)], [rd.random() for i in range(self.numFabricatorGoods)]]
    elif scenario == 'all':
      keys            = ['factory_0', 'fabricator_1']
      inventoryGoods  = [self.numFactoryGoods, self.numFabricatorGoods]
      goodConstants   = [[0.5 for i in range(self.numFactoryGoods)], [0.5 for i in range(self.numFabricatorGoods)]]

    # array to keep track of producer profits
    profits = dict()
    profits[keys[0]] = np.zeros(self.simLength)
    profits[keys[1]] = np.zeros(self.simLength)

    # initialize producers based on testCase
    if testCase == 'constantIDs':
      producers = [
        Producer(keys[0], [Good(goodConstants[0][i], rd.uniform(0.4, 0.6)) for i in range(inventoryGoods[0])]),
        Producer(keys[1], [Good(goodConstants[1][i], rd.uniform(0.5, 0.7)) for i in range(inventoryGoods[1])])
      ]
    elif testCase == 'constantPrices':
      producers = [
        Producer(keys[0], [Good(rd.uniform(0.4, 0.6), goodConstants[0][i]) for i in range(inventoryGoods[0])]),
        Producer(keys[1], [Good(rd.uniform(0.5, 0.7), goodConstants[1][i]) for i in range(inventoryGoods[1])])
      ]
    elif testCase == 'noConstants':
      producers = [
        Producer(keys[0], [Good(rd.uniform(0.4, 0.6), rd.uniform(0.5, 0.7)) for i in range(inventoryGoods[0])]),
        Producer(keys[1], [Good(rd.uniform(0.5, 0.7), rd.uniform(0.4, 0.6)) for i in range(inventoryGoods[1])])
      ]

    # return producers and profits array
    return producers, profits


###############################################################################
# RUN METHOD
###############################################################################

  # numTrials  (int)
  # testCase   (str)
  # outputFile (str)
  # monitor    (boolean)
  def run(self, numTrials = 1, testCase = 'constantIDs', scenario = 'factories', buyingDecision = 'nonRoulette', outputFile = 'validate', monitor = False):

    # let user know simulation has started running
    print "Running..."
    print ""

    # timing how long the trials take to run
    startTrial = time.clock()

    # initialize data structures for trials
    producerData = dict()
    wins = np.zeros(2)

    for trial in range(numTrials):

      # timing how long the simulation takes to run
      startSim = time.clock()

      # initialize producers
      producers, profits = self.initialize_producers(testCase, scenario)

      # run simulation
      goodsDemanded = np.zeros(self.numConsumers * self.simLength) # keeping track of goods demanded
      for timestep in range(self.simLength):
        for numConsumer in range(self.numConsumers):
          goodDemanded = rd.random()
          goodsDemanded[numConsumer + (self.numConsumers * timestep)] = goodDemanded
          self.consumerBuysFrom(producers, goodDemanded, buyingDecision)
        for producer in producers:
          profits[producer.getID()][timestep] = producer.getProfits()

      # calculate the average good demanded
      averageGoodDemanded = sum(goodsDemanded) / len(goodsDemanded)

     #Prepare data to be written to file in JSON format
      producerData.update({
        "simulation_" + str(trial + 1) :
          [{
            "producerID"       : producer.getID(),
            "profits"          : producer.getProfits(),
            "average_price"    : producer.getAverageGoodPrice(),
            "average_distance" : abs(producer.getAverageGoodID() - averageGoodDemanded)
          } for producer in producers]
      })

      # timing how long the simulation takes to run
      endSim = time.clock()

      if monitor == True:
        self.monitorSim(producers, profits, averageGoodDemanded, startSim, endSim, trial)

      # add a win to the producer with the most profits
      wins[int(max(profits, key = lambda key: sum(profits[key])).split('_')[-1])] += 1

    # timing how long the trials take to run
    endTrial = time.clock()

    # write data to file in JSON format
    write_json('../results/' + outputFile, producerData)

    # print the results of trial runs to console
    print "=================================================\n"
    print "Input parameters were:\n"
    print "SIMLENGTH = {simLength}\nNUMGOODS = {numGoods}\nNUMCONSUMERS = {numConsumers}".format(
      simLength      = SIMLENGTH,
      numGoods       = NUMGOODS,
      numConsumers   = NUMCONSUMERS,
      percentFactory = PERCENTFACTORY
    )
    print ""
    print "Test Case was: " + testCase + "\n"
    print "Scenario was: " + scenario + "\n"
    print "Results for " + str(numTrials) + " trial(s):\n"
    for producer in producers:
      print producer.getID() + " won " + str(wins[int(producer.getID().split('_')[-1])]) + " time(s)\n"
    print "Trials took " + str(endTrial - startTrial) + " seconds to run!"
    print ""
    print "================================================="


###############################################################################
# RUN SIM
###############################################################################

# command-line running of python script
if __name__ == "__main__":
  import sys
  outputFile = sys.argv[1]
  inputs = read_json('../inputs/' + sys.argv[1])

  # set simulation parameters
  SIMLENGTH      = inputs['SIMLENGTH']
  NUMGOODS       = inputs['NUMGOODS']
  NUMCONSUMERS   = inputs['NUMCONSUMERS']
  PERCENTFACTORY = inputs['PERCENTFACTORY']

  # Instantiate simulation
  validate_sim = Validate(SIMLENGTH, NUMGOODS, NUMCONSUMERS, PERCENTFACTORY)

  validate_sim.run(
    numTrials      = inputs['numTrials'],
    testCase       = inputs['testCase'],
    scenario       = inputs['scenario'],
    buyingDecision = inputs['buyingDecision'],
    outputFile     = outputFile,
    monitor        = inputs['monitor']
  )
