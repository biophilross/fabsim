# fabsim
======

### Personal Fabricator Simulation

The following terms are important when considering each prototype file and what it contains.

##### Modules Needed

These are the modules that will be needed in order to run the prototype file.

##### Good Class

This class defines what a good is. In each prototype file a good has certain attributes and methods.

##### Producer Class

This classes defines what a producer is and what a producer can do. In each prototype file a producer has certain attributes and methods.

##### Simulation Class

This class is used to instantiate a simulation object and run simulation based on the parameters passed to it during instantiation. In each prototype file the simulation class may take different inputs and may include additional functionality in terms of its methods.

##### Mathematical Model

This is the equation being used to calculate the 'probability' of a consumer purchasing a good from a certain producer. The 'probability' returned is not currently bound between 0 and 1 and the higher the 'probability' the more likely that good will be bought. This is always located in the calcProbabilityDensity() method.

##### ConsumerBuysFrom Method

This is the way in which a consumer is deciding on which good to buy based on the 'probabilities' provided by the mathematical model. There are currently two possible methods to choose from:

consumerBuysFrom() and rouletteConsumerBuysFrom()

In consumerBuysFrom() a consumer will simply buy the good with the highest 'probability' assigned to it.

In rouletteConsumerBuysFrom a consumer will use the 'probabilities' as weights to decide which good to choose. A good with a higher 'probability' has a higher liklehood of being chosen but it's not guaranteed as it is in consumerBuysFrom().

##### Goods Demanded

Here it will describe how goods are being demanded by consumers.

##### GoodIDs

This will describe whether goodIDs are initialized at random meaning does every producer sell different goods or are they the same for every producer, meaning do they all sell the same goods.

##### Pricing

Similar to GoodIDs this will indicate whether producers are selling goods for the same price or different prices.

##### Additional Functionality

This will simply describe any additional functionality that each prototype has.

#### Prototype_1.py

###### Modules Needed

    from __future__ import division # will always return floating point
    import time                     # for timing the simulation
    import os                       # interface with operating system
    import random as rd             # random number generator
    import numpy as np              # numerical functionality
    
###### Good Class

Attributes

* ID
* Price

Methods

* getID()
* getPrice()

###### Producer Class

Attributes

* ID
* Inventory
* Profits

Methods

* getID()
* getInventory()
* getProfits()
* getAverageGoodPrice()
* getAverageGoodID()
* getClosestTo()
* sell()
* __str__()

###### Simulation Class

Inputs

* Simulation Length
* Number of Consumers
* Number of Goods
* Percentage of Goods that a Factory can Producer


Methods

* calcProbDensity()
* consumerBuysFrom()
* run()

Note: Within Run Method there is a display_stats() method for debugging purposes which will print information to the console every time a simulation is run.

###### Mathematical Model

p = (1 / (t - m)**2) * (1 / c_m)

###### ConsumerBuysFrom Method

consumerBuysFrom()

###### Goods Demanded

Goods demanded are constant within this simulation. That means that each consumer will constantly choose the same good to buy every turn. Meaning that the producer who is selling the good closest to the good being demanded every turn for the cheapest price should win every single time.

##### GoodIDs

GoodIDs are constant for every producer.

###### Pricing

Every producer is selling good for different prices.

###### Additional Functionality

There is a display_results() at the end of the file that will run the simulation 50 times and tell you how often the producer selling the good closest to the good being demanded for the cheapest price wins the profit war.

#### Prototype_2.py

###### Modules Needed

    from __future__ import division # will always return floating point
    import json                     # for encoding and decoding data
    import time                     # for timing the simulation
    import os                       # interface with operating system
    import random as rd             # random number generator
    import numpy as np              # numerical functionality
    import matplotlib.pyplot as plt # plotting
    
    
###### Good Class

Attributes

* ID
* Price

Methods

* getID()
* getPrice()

###### Producer Class

Attributes

* ID
* Inventory
* Profits

Methods

* getID()
* getInventory()
* getProfits()
* getAverageGoodPrice()
* getAverageGoodID()
* getClosestTo()
* sell()
* __str__()

###### Simulation Class

Inputs

* Simulation Length
* Number of Consumers
* Number of Producers
* Number of Goods
* Percentage of Goods that a Factory can Producer

Methods

* calcProbDensity()
* consumerBuysFrom()
* write_json()
* read_json()
* plot()
* run()

Note: Within Run Method there is a display_stats() method for debugging purposes which will print information to the console every time a simulation is run.

###### Mathematical Model

p = (1 / (t - m)**2) * (1 / c_m)

###### ConsumerBuysFrom Method

consumerBuysFrom()

###### Goods Demanded

Goods demanded are randomly generated every time it becomes a consumer's turn to purchase an item.

###### GoodIDs

GoodIDs are constant for every producer.

###### Pricing

Every producer is selling good for different prices.

###### Additional Functionality

This file also has a display_results() method at the end of the file but it is not currently set to automatically run. Instead each simulation produces a plot. In addition data is actually being written to a file in JSON format each time a simulation is run. This can be found in the run() method.
