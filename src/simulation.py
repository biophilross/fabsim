#!/usr/bin/env python

###############################################################################
# PROTOTYPE

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

# CONTENTS

# IMPORT MODULES
# SIMULATION CLASS
# RUN SIM
###############################################################################


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
from utility.plot import plot
from utility.file_io import read_json, write_json

###############################################################################
# DEFINE SIMULATION CLASS
###############################################################################

class Simulation:
  #simLength (int)
  #numGoods (int)
  #numConsumers (int)
  def __init__(self, simLength, numGoods, numConsumers, numProducers, percentFactory):
    self.simLength = simLength
    self.numGoods = numGoods
    self.numConsumers = numConsumers
    self.numProducers = numProducers
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
  def rouletteConsumerBuysFrom(self, producers, goodDemanded):
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

  # scenario(str)
  def initialize_producers(self, scenario):

    # initialize producers and arrays for plotting based on scenario
    producers = []
    profits = dict()
    if scenario == 'factories':
      for i in range(self.numProducers):
        inventory = [Good(rd.random(), rd.random()) for good in range(self.numFactoryGoods)] # set inventory
        key = 'factory_' + str(i) # set key and id
        producers.append(Producer(key, inventory))
        profits[key] = np.zeros(self.simLength)
    elif scenario == 'fabricators':
      for i in range(self.numProducers):
        inventory = [Good(rd.random(), rd.random()) for good in range(self.numFabricatorGoods)] # set inventory
        key = 'fabricator_' + str(i) # set key and id
        producers.append(Producer(key, inventory))
        profits[key] = np.zeros(self.simLength)
    elif scenario == 'all':
      for i in range(int(self.numProducers / 2)):
        inventory = [Good(rd.random(), rd.random()) for good in range(self.numFactoryGoods)] # set inventory
        key = 'factory_' + str(i) # set key and id
        producers.append(Producer(key, inventory))
        profits[key] = np.zeros(self.simLength)
      for i in range(int(self.numProducers / 2)):
        inventory = [Good(rd.random(), rd.random()) for good in range(self.numFabricatorGoods)] # set inventory
        key = 'fabricator_' + str(i) # set key and id
        producers.append(Producer(key, inventory))
        profits[key] = np.zeros(self.simLength)

    # return producers and profits array
    return producers, profits


###############################################################################
# RUN METHOD
###############################################################################

  # numTrials  (int)
  # testCase   (str)
  # scenario   (str)
  # outputFile (str)
  # monitor    (boolean)
  def run(self, numTrials = 1, scenario = 'factories', outputFile = 'test', monitor = False): 

    # let user know simulation has started running
    print "Running..."
    print ""

    # timing how long the trials take to run
    startTrial = time.clock()

    # initialize data structures for trials
    producerData = dict()
    wins = np.zeros(self.numProducers)

    for trial in range(numTrials):

      # timing how long the simulation takes to run
      startSim = time.clock()

      # initialize producers, profits
      producers, profits = self.initialize_producers(scenario)

      # run simulation
      goodsDemanded = np.zeros(self.numConsumers * self.simLength) # keeping track of goods demanded
      for timestep in range(self.simLength):
        for numConsumer in range(self.numConsumers):
          goodDemanded = rd.random()
          goodsDemanded[timestep + (self.simLength * trial)] = goodDemanded
          self.rouletteConsumerBuysFrom(producers, goodDemanded)
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

      wins[int(max(profits, key = lambda key: sum(profits[key])).split('_')[-1])] += 1

      # timing how long the simulation takes to run
      endSim = time.clock()

      # output simulation results if monitoring is turned on
      if monitor == True:
        self.monitorSim(producers, profits, averageGoodDemanded, startSim, endSim, trial)

      # plot results
      plot(producerData["simulation_" + str(trial + 1)])

    # timing how long the trials take to run
    endTrial = time.clock()

    # write data to file in JSON format
    write_json('../results/' + outputFile + '.json', producerData)

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
  inputs = read_json(sys.argv[1])

# set simulation parameters
SIMLENGTH      = inputs['SIMLENGTH']
NUMGOODS       = inputs['NUMGOODS']
NUMCONSUMERS   = inputs['NUMCONSUMERS']
NUMPRODUCERS   = inputs['NUMPRODUCERS']
PERCENTFACTORY = inputs['PERCENTFACTORY']
# Instantiate simulation
sim = Simulation(SIMLENGTH, NUMGOODS, NUMCONSUMERS, NUMPRODUCERS, PERCENTFACTORY)
# run sim
sim.run(
  numTrials  = inputs['numTrials'], 
  scenario   = inputs['scenario'],
  outputFile = inputs['outputFile'], 
  monitor    = inputs['monitor']
)

