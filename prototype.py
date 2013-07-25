###############################################################################
# PROTOTPYE
#
# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators
#
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross
###############################################################################

###############################################################################
# IMPORT MODULES
###############################################################################

from __future__ import division # will always return floating point
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
  def __init__(self, idInput, priceInput, quantityInput):
    self.goodID = idInput
    self.price = priceInput
    self.quantity = quantityInput

  def getID(self):
    return self.goodID

  def getPrice(self):
    return self.price

  def getQuantity(self):
    return self.quantity

  #quantityRequested (int)
  def decrementQuantityBy(self, quantityRequested):
    self.quantity = self.quantity - quantityRequested

  #quantityRequested (int)
  def incrementQuantityBy(self, quantityRequested):
    self.quantity = self.quantity + quantityRequested

###############################################################################
# DEFINE PRODUCER CLASS
###############################################################################

class Producer:
  #inventory (Array of Goods)
  #rate (int)
  #id (string)
  def __init__(self, inventory, rate, id):
    self.inventory = inventory
    self.rate = rate
    self.id = id
    self.profits = 0

  def getID(self):
    return self.id

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

  def getClosestTo(self, goodDemanded):
    currentGoods = [good for good in self.getInventory() if good.getQuantity() != 0]
    if currentGoods: #currentGoods is not empty
      return min(currentGoods, key = lambda good: abs(goodDemanded - good.getID()))
    else: #there is no best good because inventory is empty
      return Good(0, 0, 0)

  #good (Good object)
  def sell(self, good):
    if good in self.inventory and good.getQuantity() > 0:
      good.decrementQuantityBy(1)
      self.profits = self.profits + good.getPrice()

  def updateInventory(self):
    for good in self.inventory:
      good.incrementQuantityBy(self.rate)

  def toString(self):
    for good in self.inventory:
      print "GoodID: " + str(good.getID()) + "   Price: " + str(good.getPrice()) + "  Quantity: " + str(good.getQuantity()) + "\n"

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
  def __init__(self, simLength, numGoods, numConsumers, percentFactory, factoryRate, fabricatorRate):
    print "Running..."
    print ""
    self.simLength = simLength
    self.numGoods = numGoods
    self.numConsumers = numConsumers
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
          "probability" : self.calcProbDensity(producer, goodDemanded) / sumOfProbabilities,
          "id"          : producer.getID()
        } for producer in producers]
      bestProducer = max(normalizedProbabilities, key = lambda value: value['probability'])['producer']
      bestGood = bestProducer.getClosestTo(goodDemanded)
      bestProducer.sell(bestGood)

###############################################################################
# PLOTTING METHOD
###############################################################################

  #times (Array of Timesteps)
  #profits1 (Array of Profits from 1st Producer)
  #profits2 (Array of Profits from 2nd Producer)
  def plot(self, times, profits1, profits2):
    plot1 = plt.plot(times, profits1)
    plot2 = plt.plot(times, profits2)
    plt.legend( ('Producer 1', 'Producer 2'), loc=2)

    axes = plt.gca()
    axes.set_xlabel('Timestep')
    axes.set_ylabel('Profits')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    plt.show()

###############################################################################
# JUST FACTORIES
###############################################################################

  def factories(self): # eventually add numProducers
    # factory = Producer(self.numFactoryGoods, self.factoryRate)
    # producers = [factory1, factory2]

    # intitialize arrays to plot
    times = np.array(range(self.simLength + 1))
    profits1 = np.zeros(self.simLength + 1)
    profits2 = np.zeros(self.simLength + 1)
    goodsDemanded = []

    # set inventories
    inventories = [
    [Good(rd.random(), rd.random(), self.factoryRate) for good in range(self.numFactoryGoods)], 
    [Good(rd.random(), rd.random(), self.factoryRate) for good in range(self.numFactoryGoods)]
    ]

    # initialize producers
    factory1 = Producer(inventories[0], self.factoryRate, 'Factory1')
    factory2 = Producer(inventories[1], self.factoryRate, 'Factory2')
    producers = [factory1, factory2]

    #run simulations
    for timestep in range(self.simLength):
      print str(timestep),
      for numConsumers in range(self.numConsumers):
        goodDemanded = rd.random()
        goodsDemanded.append(goodDemanded)
        self.rouletteConsumerBuysFrom(producers, goodDemanded)
      for producer in producers:
        producer.updateInventory()
      profits1[timestep + 1] = factory1.getProfits()
      profits2[timestep + 1] = factory2.getProfits()

    averageGoodDemanded = sum(goodsDemanded) / len(goodsDemanded)

    # display winner
    print "\n"
    print "=================================================="
    if factory1.getProfits() > factory2.getProfits():
      print factory1.getID() + " Wins!\n"
    else:
      print factory2.getID() + " Wins!\n"

    # display stats
    print factory1.getID() + " Profits: " + str(factory1.getProfits())
    print factory1.getID() + " Average Price: " + str(factory1.getAverageGoodPrice())
    print factory1.getID() + " Average Good Distance: " + str(abs(factory1.getAverageGoodID() - averageGoodDemanded))
    #factory1.toString()
    print ""
    print factory2.getID() + " Profits: " + str(factory2.getProfits())
    print factory2.getID() + " Average Price: " + str(factory2.getAverageGoodPrice())
    print factory2.getID() + " Average Good Distance: " + str(abs(factory2.getAverageGoodID() - averageGoodDemanded))
    print "================================================="
    #factory2.toString()
    # plot results
    #self.plot(times, profits1, profits2)

###############################################################################
# JUST FABRICATORES
###############################################################################

  def fabricators(self): # eventually add numProducers
    # fabricator = Producer(self.numFabricatorGoods, self.fabricatorRate)
    # producers = [fabricator1, fabricator2]

    # initialize arrays to plot
    times = np.array(range(self.simLength + 1))
    profits1 = np.zeros(self.simLength + 1)
    profits2 = np.zeros(self.simLength + 1)

    # set inventories
    inventories = [
    [Good(rd.random(), rd.random(), self.fabricatorRate) for good in range(self.numFabricatorGoods)], 
    [Good(rd.random(), rd.random(), self.fabricatorRate) for good in range(self.numFabricatorGoods)]
    ]

    fabricator1 = Producer(inventories[0], self.fabricatorRate, 'Fabricator1')
    fabricator2 = Producer(inventories[1], self.fabricatorRate, 'Fabricator2')
    producers = [fabricator1, fabricator2]

    for timestep in range(self.simLength):
      print str(timestep),
      print ""
      for numConsumers in range(self.numConsumers):
        self.consumerBuysFrom(producers)
      for producer in producers:
        producer.updateInventory()
      profits1[timestep + 1] = fabricator1.getProfits()
      profits2[timestep + 1] = fabricator2.getProfits()

    if fabricator1.getProfits() > fabricator2.getProfits():
      print "Fabricator1 Wins!\n"
    else:
      print "Fabricator2 Wins!\n"
    print "Fabricator1 Profits: " + str(fabricator1.getProfits())
    print "Fabricator1 Average Price: " + str(fabricator1.getAverageGoodPrice())
    #fabricator1.toString()
    print ""
    print "Fabricator2 Profits: " + str(fabricator2.getProfits())
    print "Fabricator2 Average Price: " + str(fabricator2.getAverageGoodPrice())
    #fabricator2.toString()
    #self.plot(times, profits1, profits2)

###############################################################################
# FACTORIES & FABRICATORS
###############################################################################

  def factoriesAndFabricators(self): # eventually add numProducers
    # factory = Producer(self.numFactoryGoods, self.factoryRate)
    # fabricator = Producer(self.numFabricatorGoods, self.fabricatorRate)
    # producers = [factory, fabricator]

    # initialize arrays to plot
    times = np.array(range(self.simLength + 1))
    profits1 = np.zeros(self.simLength + 1)
    profits2 = np.zeros(self.simLength + 1)

    # set inventories
    inventories = [
    [Good(rd.random(), rd.random(), self.factoryRate) for good in range(self.numFactoryGoods)], 
    [Good(rd.random(), rd.random(), self.fabricatorRate) for good in range(self.numFabricatorGoods)]
    ]

    factory = Producer(inventories[0], self.factoryRate, 'Factory')
    fabricator = Producer(inventories[1], self.fabricatorRate, 'Fabricator')
    producers = [factory, fabricator]

    for timestep in range(self.simLength):
      print str(timestep),
      print ""
      for numConsumers in range(self.numConsumers):
        self.consumerBuysFrom(producers)
      for producer in producers:
        producer.updateInventory()
      profits1[timestep + 1] = factory.getProfits()
      profits2[timestep + 1] = fabricator.getProfits()

    if factory.getProfits() > fabricator.getProfits():
      print factory.getID() + " Wins!\n"
    else:
      print fabricator.getID() + " Wins!\n"
    print factory.getID() + " Profits: " + str(factory.getProfits())
    print factory.getID() + " Average Price: " + str(factory.getAverageGoodPrice())
    #factory.toString()
    print ""
    print fabricator.getID() + " Profits: " + str(fabricator.getProfits())
    print fabricator.getID() + " Average Price: " + str(fabricator.getAverageGoodPrice())
    print ""
    #fabricator.toString()
    #self.plot(times, profits1, profits2)

###############################################################################
# RUN SIM
###############################################################################

SIMLENGTH = 100
NUMGOODS = 100
NUMCONSUMERS = 1000
PERCENTFACTORY = 0.1
FACTORYRATE = 100
FABRICATORRATE = 10
sim = simulation(SIMLENGTH, NUMGOODS, NUMCONSUMERS, PERCENTFACTORY, FACTORYRATE, FABRICATORRATE)

sim.factories()