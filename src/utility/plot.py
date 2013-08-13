#!/usr/bin/env python

# Agent-Based Simulation - Diffusion & Adoption of Personal Fabricators - PROTOTYPE
# Original Author: Wyman Zhao
# Contributor(s): Philipp Ross

"""
This file contains the plotting function used in simulation.py to display the
producerData dictionary which is also written to a results file in JSON
format.
"""

###############################################################################
# IMPORT MODULES
###############################################################################

import numpy as np              # numerical functionality
import matplotlib.pyplot as plt # plotting

###############################################################################
# PLOTTING METHOD
###############################################################################

#producers (List of Dictionaries of Producers)
def plot(producerData):
  "Reformats producerData into arrays to be plotted using matplotlib module."
  # format data
  producerIDs = [int(producer['producerID'].split('_')[-1]) for producer in producerData]
  profits = [producer['profits'] for producer in producerData]
  average_prices = [producer['average_price'] for producer in producerData]
  average_distances = [producer['average_distance'] for producer in producerData]

  # determine figure size - figsize(1,1) = 1" x 1" or 80 pixels x 80 pixels
  plt.figure(1, figsize=(12, 8))

  # plot profits
  plt.subplot(311)
  plt.grid(True)
  plt.title('Profits')
  plt.ylabel('Profits')
  plt.xlabel('ProducerIDs')
  plt.axis([0, len(producerIDs) - 1 , 0, max(profits)])
  plt.fill_between(producerIDs, profits, alpha='0.6', color='blue')
  plt.plot(producerIDs, profits, 'k')

  # plot average_prices
  plt.subplot(312)
  plt.grid(True)
  plt.title('Average Good Price')
  plt.ylabel('Average Price')
  plt.xlabel('ProducerIDs')
  plt.axis([0, len(producerIDs) - 1, 0, 1])
  plt.fill_between(producerIDs, average_prices, alpha='0.6', color='blue')
  plt.plot(producerIDs, average_prices, 'k')

  # plot average_distances
  plt.subplot(313)
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