## Source Code Overview

This file gives a more technical and code specific description of the simulation as opposed to the conceptual model description found in __sim_overview.md__.

### Contents

1. Project Directory Structure
2. Differences between validate.py & simulation.py
3. What is JavaScript Object Notation?
4. Buying Decision Algorithms

### Project Directory Structure

Currently the project is broken up into the directories doc, inputs, results, and src. doc contains any documentation necessary to understand the simulation prototype package, inputs contains the input files to use when running each simulation in JSON format, results  the results of the input file with the same name, and src contains the actual source code split up into separate modules for the sake of modularity. 

Each class is broken up into it's own file and is found within the main src directory. Any additional functions such as file input/output and plotting can be found in the utility directory.

##### IMPORTANT 
Make sure you keep the same directory structure when downloading the project from github. If you want to change the directory structure make sure you look into the source code to edit where to find input files and where to put output files. The same goes for where to find source code files.

### Differences Between validate.py & simulation.py

Currently there are two files with which to run simulations. One of them is called _validate.py_ and one of them is called _simulation.py_. They can both be used to run simulations and are very similar but contain a few differences that should be of note.

First off, _validate.py_ has a different purpose than _simulation.py_. _validate.py_ is being used to validate initial model assumptions and the mathematical model being applied and described in __sim_overview.md__. 

Within _validate.py_ you are limited to two producers. Your simulation can either consist of two factories, two fabricators, or one of each depending on the input supplied.

You can choose whether to use a deterministic buying algorithm for consumers or whether to use a roulette-based decision making algorithm. Within _simulation.py_ you can currently only use the roulette-based algorithm.

You can choose explicitly which test case you want to look at. The different test cases are defined within __sim_overview.md__. In _simulation.py_ you have to hardcode the values in yourself if you want to run the simulation under different test cases.

And finally, _validate.py_ currently contains no plotting ability. That ability is restricted to _simulation.py_. 

This means that there are additional inputs that need to be added to the inputs.json file used with _validate.py_. These inputs include 'testCase' and 'buyingDecision'. 

'testCase' can either be:

1. 'constantIDs'
2. 'constantPrices'
3. 'noConstants'

This is just telling you which values are to be consistent across producers. So for example in 'testCase' 1 each producer would be selling the same goods meaning they were all generated using the same goodIDs whereas in 'testCase' 3 each producer was initialized with unique values.

'buyingDecision' can either be:

1. 'nonRoulette'
2. 'roulette'

This simply defines which algorithm to use when consumers make a buying decision. Both are defined within _validate.py_. 

### What is Javascript Object Notation?

Javascript Object Notation (or JSON for short) is a popular format used when transmitting data through web applications. It's especially lightweight and fairly intuitive to structure as it follows a basic key value pairing format similar to python's dictionary data structure thus making it extremely compatible when used together with python.

The only downside is that to the human eye, it's not very readable unless formatted by some kind of JSON formatting tool. However, these tools can be easily found using some Google-fu.

Here's one example: [JSON Viewer](http://jsonviewer.stack.hu/)

Simply copy and paste the entire JSON file into the window.

### Buying Decision Algorithms

Currently _validate.py_ has two buying methods to choose from. One is roulette() and the other is nonRoulette(), meaning it's deterministic.

nonRoulette() just calculates the probability densities for each producer based on the goodDemanded as described by the mathematical model in __sim_overview.md__ and then chooses the producer with the highest probability density.

roulette() on the other hand uses the probability densities calculated for each producer as weights. An analogy would be as if you had a spin wheel with an arrow on it and composed of different colors - each color representing a different producer. The area that each color takes up on the color wheel is directly proportional to probability density calculated for each producer. Then the algorithm basically spins the wheel to decide which producer to buy from. The producer with a higher probability density will have a much higher likelyhood of being chosen but it's not a definite as it would be using the nonRoulette() method.



